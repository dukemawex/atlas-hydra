from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Any
import httpx


def lit(v: Any) -> str:
    return "'" + str(v).replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ") + "'"

@dataclass
class Atlas:
    base: str = os.getenv("HYDRA_URL", "http://127.0.0.1:8443")
    token: str = os.getenv("HYDRA_TOKEN", "local-development-token-32-bytes")
    graph: str = os.getenv("HYDRA_GRAPH", "default")
    cell: str = os.getenv("HYDRA_CELL", "cell-0")
    collection: str = os.getenv("HYDRA_COLLECTION", "atlas")

    @property
    def hosted(self) -> bool:
        return self.base.startswith("https://")

    async def ingest_text(self, text: str, title: str = "atlas-demo") -> dict:
        import json
        files = {"memories": (None, json.dumps([{"text": text, "infer": False, "title": title}]))}
        data = {"type": "memory", "database": self.graph, "collection": self.collection, "upsert": "true"}
        headers = {"Authorization": f"Bearer {self.token}", "API-Version": "2"}
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(f"{self.base.rstrip('/')}/context/ingest", headers=headers, data=data, files=files); r.raise_for_status(); return r.json()

    async def cypher(self, query: str) -> dict:
        async with httpx.AsyncClient(timeout=30) as c:
            if self.hosted:
                r = await c.post(f"{self.base.rstrip('/')}/query", headers={"Authorization": f"Bearer {self.token}", "API-Version": "2"}, json={"database": self.graph, "collection": self.collection, "query": query, "type": "all", "mode": "thinking", "graph_context": True})
            else:
                r = await c.post(f"{self.base}/v1/graphs/{self.graph}/query", headers={"Authorization": f"Bearer {self.token}", "X-Graph-Namespace": "default"}, json={"cell_id": self.cell, "query": query})
            r.raise_for_status(); return r.json()

    async def ingest_fixture(self):
        if self.hosted:
            return await self.ingest_text("""Atlas fixture: Sam, @sam, and S. Ratnaparkhi are the same person. Sam owns Phoenix. A Slack claim says Phoenix is ready to launch, but a later Drive claim says Phoenix is blocked on security review. The later claim supersedes the earlier claim. Apollo ownership is not present in this fixture.""", "atlas-enterprise-demo")
        return await self.cypher("""
        CREATE
        (sam:Person {id:'p-sam', canonical:'Sam Ratnaparkhi'}),
        (d:Document {id:'d-slack-1', source:'slack', at:'2026-08-12T09:00:00Z'}),
        (d2:Document {id:'d-drive-1', source:'drive', at:'2026-08-11T09:00:00Z'}),
        (p:Project {id:'proj-phoenix', name:'Phoenix'}),
        (c1:Claim {id:'c1', text:'Phoenix is ready for launch', truth:'disputed', at:'2026-08-12T09:00:00Z', authority:0.8}),
        (c2:Claim {id:'c2', text:'Phoenix is blocked on security review', truth:'current', at:'2026-08-12T10:00:00Z', authority:0.95}),
        (alias:PersonAlias {value:'@sam'}),
        (alias)-[:RESOLVES_TO]->(sam), (sam)-[:OWNS]->(p),
        (c1)-[:ABOUT]->(p), (c2)-[:ABOUT]->(p),
        (c1)-[:SUPPORTED_BY]->(d), (c2)-[:SUPPORTED_BY]->(d2),
        (c2)-[:SUPERSEDES]->(c1)
        """)

    async def resolve(self, project: str):
        return await self.cypher(f"""
        MATCH (p:Project {{name:{lit(project)}}})<-[:ABOUT]-(c:Claim)
        OPTIONAL MATCH (c)-[:SUPPORTED_BY]->(d:Document)
        RETURN c.text AS claim, c.truth AS truth, c.at AS observed_at,
               c.authority AS authority, collect(d.source) AS sources
        ORDER BY c.authority DESC, c.at DESC
        """)

    async def aliases(self, value: str):
        return await self.cypher(f"""
        MATCH (a:PersonAlias {{value:{lit(value)}}})-[:RESOLVES_TO]->(p:Person)
        RETURN p.canonical AS canonical
        LIMIT 1
        """)

    async def missing(self, question: str):
        return {"status": "NOT_FOUND", "question": question, "evidence": []}
