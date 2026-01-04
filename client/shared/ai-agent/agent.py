#!/usr/bin/env python3
"""
MANVA AI Agent — deterministic + light-weight actions for local use.

Endpoints:
- POST /intent   { "text": "search rust guides" } -> classification
- POST /action/summarize { "url": "https://..." } -> fetch & summarize
- GET  /health
"""
from flask import Flask, request, jsonify
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import re

app = Flask("manva_ai_agent")

def classify_intent(text: str):
    t = (text or "").strip()
    l = t.lower()
    if l.startswith("search "):
        return {"intent": "search", "query": t[len("search ") :].strip()}
    if l.startswith("open "):
        return {"intent": "open", "target": t[len("open ") :].strip()}
    if "summarize" in l or "summary" in l:
        return {"intent": "summarize"}
    # fallback: url
    m = re.search(r"https?://[^\s]+", t)
    if m:
        return {"intent": "open", "url": m.group(0)}
    return {"intent": "unknown"}

@app.route("/intent", methods=["POST"])
def intent():
    data = request.get_json(force=True)
    text = data.get("text", "")
    res = classify_intent(text)
    return jsonify({"ok": True, "result": res})

@app.route("/action/summarize", methods=["POST"])
def summarize():
    data = request.get_json(force=True)
    url = data.get("url") or data.get("target")
    if not url:
        return jsonify({"ok": False, "error": "missing url"}), 400
    try:
        # simple fetch with timeout and UA
        r = requests.get(url, timeout=6, headers={"User-Agent": "Manva-Agent/0.1"})
        r.raise_for_status()
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    # parse and extract paragraphs
    soup = BeautifulSoup(r.text, "html.parser")
    # remove scripts/styles
    for s in soup(["script", "style", "noscript"]):
        s.decompose()

    # prefer article tags
    content_candidates = soup.find_all("article")
    paragraphs = []
    if content_candidates:
        for cand in content_candidates:
            paragraphs += [p.get_text().strip() for p in cand.find_all("p")]
    if not paragraphs:
        paragraphs = [p.get_text().strip() for p in soup.find_all("p")]

    # join and make a naive extractive summary: pick top 3 longest sentences
    textblob = "\n\n".join([p for p in paragraphs if p])
    sentences = re.split(r'(?<=[.!?])\s+', textblob)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    # rank by length (simple heuristic)
    sentences = sorted(sentences, key=lambda s: len(s), reverse=True)
    summary = "\n\n".join(sentences[:3]) if sentences else (textblob[:800] + "...")
    return jsonify({"ok": True, "summary": summary})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "status": "ready"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
