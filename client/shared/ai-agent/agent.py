from flask import Flask, request, jsonify

app = Flask("manva_ai_agent")


def classify_intent(text: str):
    # Very small deterministic stub — replace with on-device model later.
    t = text.strip().lower()
    if t.startswith("search "):
        return {"intent": "search", "query": t[len("search "):].strip()}
    if t.startswith("open "):
        return {"intent": "open", "target": t[len("open "):].strip()}
    if "summarize" in t or "summary" in t:
        return {"intent": "summarize"}
    return {"intent": "unknown"}


@app.route("/intent", methods=["POST"])
def intent():
    data = request.get_json(force=True)
    text = data.get("text", "")
    res = classify_intent(text)
    return jsonify({"ok": True, "result": res})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "status": "ready"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
