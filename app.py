import json
import urllib.request
import traceback
import os

OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")
MODEL = "mistralai/mistral-nemo"

def application(environ, start_response):
    path = environ.get("PATH_INFO", "")

    if path == "/ping":
        start_response("200 OK", [("Content-Type", "application/json")])
        return [b'{"status":"alive"}']

    try:
        length = int(environ.get("CONTENT_LENGTH") or 0)

        if length == 0:
            response_body = json.dumps({"error": "empty body"}).encode("utf-8")
            start_response("400 Bad Request", [("Content-Type", "application/json")])
            return [response_body]

        body = environ["wsgi.input"].read(length)
        data = json.loads(body)
        messages = data.get("messages", [])

        payload = json.dumps({
            "model": MODEL,
            "messages": messages,
            "max_tokens": 150,
            "temperature": 0.9,
            "frequency_penalty": 1.2
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
        error_body = json.dumps({"error": str(e)}).encode("utf-8")
        start_response("500 Internal Server Error", [("Content-Type", "application/json")])
        return [error_body]
