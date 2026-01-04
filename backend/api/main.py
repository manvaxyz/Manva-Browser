from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

AI_AGENT = os.getenv("AI_AGENT_URL", "http://127.0.0.1:8080")

app = FastAPI(title="Manva API Gateway")

class IntentIn(BaseModel):
    text: str

@app.get("/health")
def health():
    return {"ok": True, "status": "ready"}

@app.post("/intent")
def proxy_intent(payload: IntentIn):
    try:
        r = requests.post(f"{AI_AGENT}/intent", json={"text": payload.text}, timeout=5)
        r.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    return r.json()

@app.post("/action/summarize")
def proxy_summarize(body: dict):
    try:
        r = requests.post(f"{AI_AGENT}/action/summarize", json=body, timeout=15)
        r.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    return r.json()
