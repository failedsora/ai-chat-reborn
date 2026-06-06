import json
import urllib.request
import traceback

OPENROUTER_KEY = "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"
MODEL = "mistralai/mistral-nemo"

def application(environ, start_response):
    try:
        length = int(environ.get("CONTENT_LENGTH") or 0)
        body = environ["wsgi.input"].read(length)
        data = json.loads(body)
        messages = data.get("messages", [])

        payload = json.dumps({
            "model": MODEL,
            "messages": messages
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://ai-chat-reborn.onrender.com",
                "X-Title": "AI Chat Reborn"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=30) as res:
            result = json.loads(res.read())

        reply = result["choices"][0]["message"]["content"]
        response_body = json.dumps({"reply": reply}).encode("utf-8")
        start_response("200 OK", [("Content-Type", "application/json")])
        return [response_body]

    except Exception as e:
        tb = traceback.format_exc()
        print("ERROR:", tb)
        error_body = json.dumps({"error": str(e), "trace": tb}).encode("utf-8")
        start_response("500 Internal Server Error", [("Content-Type", "application/json")])
        return [error_body]
