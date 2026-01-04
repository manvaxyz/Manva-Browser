MANVA AI Agent

This agent provides:
- Deterministic intent classification
- Summarization action (fetch + naive extractive summarizer)
- Simple HTTP API for local-first usage

Run locally:
- ./run_local_agent.sh

Docker:
- docker build -t manva-ai-agent -f Dockerfile.agent .

Notes:
- This is intentionally small and deterministic to run on-device.
- Replace with on-device GGML/ONNX model later; ensure same endpoints.
