# Atlas — enterprise decision graph

Hack Hydra Track 1 submission. Atlas ingests noisy enterprise records into HydraDB and answers ownership, decision, and contradiction questions with traceable graph paths.

## Demo

The included fixture contains aliases for one person, contradictory project status claims, and a missing fact. The demo shows entity resolution, conflict-aware current truth, provenance, and explicit `NOT_FOUND`.

```bash
python -m venv .venv && .venv/bin/pip install -e .
HYDRA_URL=http://127.0.0.1:8443 .venv/bin/python demo.py
```

## HydraDB is core

Atlas uses HydraDB as the source of truth for `Person`, `Project`, `Document`, `Claim`, and `Decision` nodes and their `OWNS`, `ABOUT`, `SUPPORTS`, `CONTRADICTS`, and `SUPERSEDES` edges. Its answer path is a bounded OpenCypher traversal, not a vector lookup.

HydraDB: https://github.com/hydra-db/hydradb
Hack Hydra: https://hackhydra.hydradb.com
