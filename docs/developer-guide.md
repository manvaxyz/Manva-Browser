Developer Guide (quickstart)

1) Build desktop prototype

```bash
cd client/desktop
cargo build
```

2) Run ai-agent locally

```bash
cd client/shared/ai-agent
./run_local_agent.sh
```

3) Run local pipeline

```bash
./ops/ci/run-local-pipeline.sh
```

Replace stubs with production components per docs/architecture.md.
