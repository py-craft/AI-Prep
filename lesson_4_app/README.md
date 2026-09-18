# Lesson 4 — Layered FastAPI order assistant

From the repository root, install dependencies and ensure `.env` contains a
non-empty `OPENAI_API_KEY`. Then use two terminals:

```bash
python order_mcp_server.py
```

```bash
uvicorn lesson_4_app.app.main:app --reload --port 8001
```

Open `http://127.0.0.1:8001/docs`, or call:

```bash
curl -X POST http://127.0.0.1:8001/api/v1/orders/ask \
  -H 'Content-Type: application/json' \
  -d '{"question":"What is happening with order A100?"}'
```

Application prompts live in `app/prompts/order_assistant.yml`. They are loaded
with `yaml.safe_load`, validated at the dependency boundary, and cached.
