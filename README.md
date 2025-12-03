# Byte Server API

FastAPI service that generates programming quiz questions using an Ollama-compatible model.

## Endpoint

POST `/quiz/generate`

- Description: Generate programming quiz questions. Supports streaming text output or structured JSON.
- Consumes: `application/json`
- Produces: `application/json` (non-stream) or `text/plain` (stream/raw fallback)

### Request body

```json
{
  "lang": "Python",
  "num_questions": 5,
  "difficulty": "medium",
  "model": "gpt-oss:20b",
  "stream": false
}
```

Fields:

- `lang` (string, required): Programming language (e.g., "Python", "JavaScript"). Must be non-empty.
- `num_questions` (integer, default: 5): Range 1–50.
- `difficulty` (string, required): One of `easy | medium | hard`.
- `model` (string, default: `gpt-oss:20b`): Ollama model identifier.
- `stream` (boolean, default: false): If true, returns a streamed plain-text response.

### Successful responses

- 200 OK (non-stream): JSON array of question objects

  ```json
  [
    {
      "question": "Which of the following ...?",
      "options": ["A", "B", "C", "D"],
      "answer": "B"
    }
  ]
  ```

- 200 OK (stream): `text/plain` where content arrives incrementally as the model generates.

- 200 OK (raw fallback): If the model returns non-JSON and parsing fails, the endpoint returns the raw content as `text/plain`.

### Error responses

- 422 Unprocessable Entity: Invalid inputs (e.g., empty `lang`, invalid `difficulty`).
- 502 Bad Gateway: Model call failed.
- 500 Internal Server Error: Empty response or malformed data that cannot be salvaged to JSON.

## Authentication

The server uses an API key for Ollama requests, set via `app.settings.settings.OLLAMA_API_KEY`. Ensure your environment provides this value.

## Quick start

1. Install dependencies and run the server (example):

   - Ensure FastAPI and `ollama` Python client are installed.
   - Export `OLLAMA_API_KEY` environment variable.
   - Run your app (e.g., via `uvicorn app.main:app --reload`).

2. Test non-stream mode (returns JSON):

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  http://localhost:8000/quiz/generate \
  -d '{
    "lang": "Python",
    "num_questions": 5,
    "difficulty": "hard",
    "model": "gpt-oss:20b",
    "stream": false
  }' | jq '.'
```

3. Test stream mode (returns text/plain stream):

```bash
curl -N -X POST \
  -H "Content-Type: application/json" \
  http://localhost:8000/quiz/generate \
  -d '{
    "lang": "Python",
    "num_questions": 5,
    "difficulty": "hard",
    "model": "gpt-oss:20b",
    "stream": true
  }'
```

Note: With `stream=true`, the response may contain JSON fragments or prose depending on the model. If you need structured data, set `stream=false`.
