#!/usr/bin/env bash
set -euo pipefail
echo "Running local pipeline: build desktop, run ai-agent health check"

echo "Building desktop prototype"
pushd client/desktop >/dev/null
cargo build --manifest-path Cargo.toml
popd >/dev/null

echo "Starting ai-agent in background"
pushd client/shared/ai-agent >/dev/null
python -m pip install --user -r requirements.txt
nohup python agent.py >/tmp/manva_ai_agent.log 2>&1 &
sleep 1
curl -sS http://127.0.0.1:8080/health
popd >/dev/null

echo "Local pipeline finished"
