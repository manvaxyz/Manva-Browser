MANVA Architecture (prototype)

This document summarizes the high-level architecture for MANVA and points to next implementation steps.

- Client: Rust-based desktop shell, Kotlin Android app, shared Rust core for renderer and AI bindings.
- AI: local-first models (GGML/ONNX) with optional cloud workers for heavy tasks.
- Backend: minimal auth, update server, model registry (signed models).

Next steps:
- Implement renderer prototype using wgpu and a minimal HTML layout engine.
- Replace agent stub with on-device inference runtime.
