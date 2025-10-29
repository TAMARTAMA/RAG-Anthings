# Chat Server (FastAPI)

This FastAPI service powers the BOTNET chat experience. It exposes chat endpoints consumed by the React UI and fans out each user request to two backends: an LLM generator and a document search service. The responses are merged and persisted to a lightweight JSON store for later retrieval and rating.

## How It Works
- `POST /api/message/add` receives a user prompt, calls the LLM to extract keywords, queries the search service, and asks the LLM again (prompted with the search results) for the final answer.
- `POST /api/message/rate` records thumbs-up/thumbs-down feedback for an existing chat entry.
- `GET /api/message/history` returns the recorded conversations.


## Requirements
- Python 3.10 or newer
- Access to the upstream LLM endpoint and search endpoint configured in `config.json`

## Quick Start
```bash
cd Server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
```

## Configuration
`config.json` sits at the project root. Key fields:
- `server.host` / `server.port`: bind address for uvicorn (default `0.0.0.0:8002`).
- `remote_server.url_LLM`: URL of the LLM generation service.
- `remote_server.url_search`: URL of the keyword-based search service.
- `chat_dir`: file path (relative or absolute) used to persist chat history as JSON. Ensure the process has write permissions.

Update the file before launching if your infrastructure differs. The FastAPI app reads this configuration at startup.

## API Reference
### `POST /api/message/add`
**Body**
```json
{
  "userId": "123",
  "request": "What is the status of project Alpha?"
}
```
**Response**
```json
{
  "answer": "...LLM response..."
}
```
Also stores the Q/A pair in the chat history file.

### `POST /api/message/rate`
**Body**
```json
{
  "userId": "123",
  "messageId": 5,
  "rating": "like"
}
```
**Response**
```json
{
  "status": "ok"
}
```
Returns `status: "error"` if the message ID is unknown.

### `GET /api/message/history`
Returns all stored chats. Example:
```json
[
  {
    "id": 5,
    "question": "...",
    "answer": "...",
    "rate": "like"
  }
]
```

## Testing the Endpoints
With the server running, use curl:
```bash
curl -X POST http://localhost:8002/api/message/add \
  -H "Content-Type: application/json" \
  -d '{"userId":"demo","request":"Hello"}'
```
