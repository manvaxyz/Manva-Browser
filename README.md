# MANVA — Manva-Browser

MANVA (मनवा) — The world’s first fully AI-controlled all-in-one browser platform.

This repository contains the initial scaffold and prototypes for MANVA: a privacy-first, local-first, AI-governed browser platform (desktop + Android) with built-in AI tools, auto-deploy and self-healing CI/CD.

Quickstart (developer):

- Build desktop prototype

```bash
cd client/desktop
cargo build
```

- Run the local AI agent (intent stub)

```bash
cd client/shared/ai-agent
./run_local_agent.sh
```

- Run the local CI pipeline (build + basic health check)

```bash
./ops/ci/run-local-pipeline.sh
```

Repository layout:

- `client/desktop` — Rust-based desktop shell prototype
- `client/android` — Android app skeleton and notes
- `client/shared/ai-agent` — local AI agent prototype (intent parsing)
- `backend/*` — backend microservice stubs (auth, update, model-registry)
- `ops/ci` — local CI pipeline scripts
- `ops/deployment` — deployment examples (k8s sample)
- `docs/` — architecture, security, developer guides

Contributing:

Follow the developer guide in `docs/developer-guide.md`. Pull requests must include tests or reproducible build steps for any core change. All releases are signed and reproducible.
# Manva-Browser