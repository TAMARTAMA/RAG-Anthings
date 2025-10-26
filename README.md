# BOTNET Chat Platform

A full-stack conversational assistant that pairs a FastAPI backend with a React + TypeScript frontend. The backend orchestrates requests to remote large language model (LLM) and document search services, persists chat history, and exposes a REST API. The frontend delivers an RTL-friendly chat experience with local persistence, rating controls, and conversation management.

## Repository Structure

```text
.
├── Server/                
│   ├── app/               
│   │   ├── routes/        
│   │   ├── services/      
│   │   ├── models/        
│   │   └── config.py      
│   ├── all_chats          
│   ├── config.json        
│   └── requirements.txt   
└── chat_UI/               
    ├── src/               
    ├── package.json       
    ├── tailwind.config.js 
    └── tsconfig*.json     
```

## Key Features

- Chatbot API that calls out to external LLM and search services.
- Flat-file storage of conversations with rating support.
- React chat interface with welcome screen, sidebar, history, and thumbs up/down feedback.
- LocalStorage caching of chats for instant UI responsiveness.

## Prerequisites

- Python 3.10+
- Node.js 18+ and npm 9+
- Network access from the backend to the remote LLM and search services defined in `Server/config.json`

## Backend Setup (`Server/`)

1. **Install dependencies**
   ```bash
   cd Server
   python -m venv .venv
   source .venv/bin/activate            
   pip install -r requirements.txt
   ```
2. **Configure runtime settings**
   - Edit `config.json` before launching the server.
   - `server.host` / `server.port`: FastAPI listening address (default `0.0.0.0:8002`).
   - `remote_server.url_LLM`: HTTP endpoint used for keyword extraction and answer generation.
   - `remote_server.url_search`: HTTP endpoint queried for relevant documents.
   - `chat_dir`: File name used for persisted history (`all_chats`).
3. **Run the API locally**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
   ```
   Interactive docs are available at `http://localhost:8002/docs`.

## Frontend Setup (`chat_UI/`)

1. **Install dependencies**
   ```bash
   cd chat_UI
   npm install
   ```
2. **Configure API base URL (optional)**
   - The frontend uses `http://localhost:8002/` by default (`src/services/api.ts`).
   - Update this file if the backend is hosted elsewhere.
3. **Run the Vite dev server**
   ```bash
   npm run dev
   ```
   Vite prints the local URL (typically `http://localhost:5173`).

## Running Locally

1. Start the FastAPI server (`uvicorn app.main:app --reload --host 0.0.0.0 --port 8002`).
2. In another terminal, start the frontend (`npm run dev`).
3. Visit the frontend URL from the Vite output to begin chatting. Ensure the browser can reach the backend host/port.

The backend writes chat history to the JSON file configured by `chat_dir` (default `Server/all_chats`). The frontend also caches chats in the browser's `localStorage` under the `chatHistory` key.

## API Reference

| Method | Path                   | Description                                   | Request Body (JSON)                                           | Response |
|--------|------------------------|-----------------------------------------------|----------------------------------------------------------------|----------|
| POST   | `/api/message/add`     | Submit a user prompt for processing           | `{ "request": "<text>", "userId": "<string>" }`                     | `{ "answer": "<text>" }` |
| POST   | `/api/message/rate`    | Record thumbs up/down feedback for a message  | `{ "userId": "<string>", "messageId": "<id>", "rating": "like" \| "dislike" \| null }` | `{ "status": "ok" }` or error |
| GET    | `/api/message/history` | Retrieve stored conversations                 | Query parameter: `userId` (currently unused in backend logic)  | `[ { "id": 1, "question": "...", "answer": "...", "rate": "..." } ]` |

The backend uses the configured LLM endpoint to derive keywords and craft final responses. If keyword extraction fails or the remote services cannot be reached, the server answers with a fallback message such as “No keywords were found that match your question.”


## Configuration & Environment

- `Server/config.json` — Update host/port and remote service URLs before deployment.
- `chat_UI/src/services/api.ts` — Adjust base API URLs for staging/production.



