import json
import urllib.request

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
                "HTTP-Referer": "https://failedsora.pythonanywhere.com",
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
        error_body = json.dumps({"error": str(e)}).encode("utf-8")
        start_response("500 Internal Server Error", [("Content-Type", "application/json")])
        return [error_body]
