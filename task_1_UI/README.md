# Moptimizer

A small chat stack composed of:
- **Server**: Node/Express API that talks to a **FastAPI** model server and stores chat history in a JSON file.
- **Client**: Vite + React frontend.

---

## 1) Project Layout
task_1_UI/
├─ Server/ # Node/Express API
│ ├─ server.js
│ ├─ Routes/
│ └─ Controllers/
│
└─ project/ # Vite + React client
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

### Server (`task_1_UI/Server/.env`)
```env
   PORT=5000
   MODEL_URL=http://127.0.0.1:8001/generate
   Optional future use:
   SECRET=change-me```
   There is an example file at:
   task_1_UI/Server/.env.example
   
### Client (task_1_UI/project/.env)
   Only variables starting with VITE_ are exposed to the browser.
   Development (local or via SSH tunnel):
   VITE_API_BASE=http://localhost:5000
   Production (public IP / domain):
   VITE_API_BASE=http://YOUR_SERVER_IP_OR_DOMAIN:5000
   There is an example file at:
   task_1_UI/project/.env.example
## 4) Running the Servers
4.1 Run the Node API (development)
   cd task_1_UI/Server
   npm i
   NODE_ENV=development npm start
   Node will listen on http://0.0.0.0:5000 (or the PORT you set).
4.2 Run the client (development)
   cd task_1_UI/project
   npm i
   npm run dev
   Open the printed URL (commonly http://localhost:5173).
5) Troubleshooting

Frontend hits localhost by mistake: Ensure VITE_API_BASE points to your Node server (IP/domain).

CORS errors in dev: Node enables cors() in development. Prefer serving client and API from the same origin in production.

Empty reply from server: Usually a crash/unhandled error in Node. Run node server.js in the foreground and watch logs.

Model returns “repetitive English text”:

Lower temperature (e.g., 0.2–0.4) and top_k (e.g., 40–60).

Make sure your prompt is exactly the user’s text (not an ID).

Use a random seed for more variation or a fixed seed for determinism.




RUN
~/B/code/SERVER/task_1_UI/project$ npm run dev


~/B/code/SERVER/task_1_UI/Server_new$ uvicorn app.main:app  --reload --port 8002


~/B$ uvicorn Moptimizer.LLM_server.server:app --host 192.168.50.3 --port 8013

~/B/data/KG/search$ uvicorn main:app --host 0.0.0.0 --port 8003