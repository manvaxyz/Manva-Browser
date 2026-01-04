# Local Developer Run Instructions (MVP)

Prereqs:
- Git, Docker and docker-compose
- Rust toolchain for desktop build (optional)
- Node 18+ and npm (for front-end dev)

1) Start everything with Docker Compose (recommended)
   docker-compose up --build

   Services:
   - ai-agent -> http://localhost:8080
   - auth-service -> http://localhost:8081
   - update-service -> http://localhost:8082
   - model-registry -> http://localhost:8083
   - api gateway -> http://localhost:8000
   - frontend (Vite) -> http://localhost:5173

2) Frontend developer flow (fast)
   cd client/web
   npm install
   npm run dev
   Open http://localhost:5173

3) AI agent (local)
   cd client/shared/ai-agent
   ./run_local_agent.sh
   Health: GET http://127.0.0.1:8080/health

4) Desktop prototype (Rust)
   cd client/desktop
   cargo build --release
   ./target/release/manva_desktop

Security notes and env:
- No keys are hard-coded. Use environment variables for production (e.g. AI_AGENT_URL, JWT secrets).
