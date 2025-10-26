# Moptimizer

A chat bot stack composed of:
- **Server**: Node/Express API that talks to a **FastAPI** model server and stores chat history in a JSON file.
- **Client**: Vite + React frontend.

---

## 1) Project Layout

SERVER/
├─ Server/ # Node/Express API
|  ├─ app/
│  | ├─ models/
│  | ├─ routes/
|  | ├─ utils/
│  | └─ services/
│  ├─ config.json
|  ├─ requirements
|
├─ chat_UI / # Vite + React client
├─ index.html
├─ src/
└─ vite.config.ts

## 2) Requirements

- **Node.js** v18+ and npm
- **Python 3.10+** (for the model server)
- A running **FastAPI model server** (default: `http://127.0.0.1:8001/generate`)

> If the model server runs on a different host or port, set `MODEL_URL` accordingly (see Environment).

---

## 3) Environment Variables

Create your own `.env` files from the examples below. **Do not commit real `.env` files**—commit only the `*.example` files.

RUN
~/B/code/SERVER/task_1_UI/project$ npm run dev

~/B/code/SERVER/task_1_UI/Server_new$ uvicorn app.main:app  --reload --port 8002

~/B$ uvicorn Moptimizer.LLM_server.server:app --host 192.168.50.3 --port 8013

~/B/data/KG/search$ uvicorn main:app --host 0.0.0.0 --port 8003