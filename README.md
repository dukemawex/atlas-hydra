# Atlas — enterprise decision graph

Hack Hydra Track 1 submission. Atlas ingests noisy enterprise records into HydraDB and answers ownership, decision, and contradiction questions with traceable graph paths.

## Demo

The included fixture contains aliases for one person, contradictory project status claims, and a missing fact. The demo shows entity resolution, conflict-aware current truth, provenance, and explicit `NOT_FOUND`.

```bash
python -m venv .venv && .venv/bin/pip install -e .
HYDRA_URL=http://127.0.0.1:8443 .venv/bin/python demo.py
```

## Built on the HydraDB open-source repo

This repository pins the HydraDB OS source as `vendor/hydradb` via a Git submodule. The hosted API is the default demo runtime; the pinned source is the local/self-hosted runtime and the reference for the graph model and OpenCypher behavior.

```bash
git clone --recurse-submodules <this-repository-url>
# or, after cloning:
git submodule update --init --recursive
```

## HydraDB is core

Atlas uses HydraDB as the source of truth for `Person`, `Project`, `Document`, `Claim`, and `Decision` nodes and their `OWNS`, `ABOUT`, `SUPPORTS`, `CONTRADICTS`, and `SUPERSEDES` edges. Its answer path is a bounded OpenCypher traversal, not a vector lookup.

HydraDB: https://github.com/hydra-db/hydradb
Hack Hydra: https://hackhydra.hydradb.com

## What Atlas loses without HydraDB

Atlas writes structured enterprise records through HydraDB `app_knowledge` and retrieves with HydraDB graph context enabled. HydraDB is responsible for entity/relation extraction and evidence paths across aliases, projects, claims, and source documents. Without it, Atlas becomes a flat document search tool: it cannot resolve `@sam` to a canonical person, traverse ownership, compare contradictory claims, or show why one claim supersedes another.

## Run the demo

```bash
pip install -e .
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000`. The UI calls HydraDB-backed alias and conflict-resolution routes.

## Submission demo

Atlas MVP demo video: `Atlas-MVP.mp4`.
