# BOTNET Chat UI

A Vite + React + TypeScript single-page app that provides a polished chat experience in Hebrew. It connects to a backend chatbot service running on `http://localhost:8002`.

## What You See
- Animated welcome screen that invites the user to start a new conversation
- Sidebar with the full chat history, quick delete and create actions, and Hebrew dates
- Chat workspace that keeps the conversation thread, shows typing states, and lets users rate bot replies
- Local storage persistence so previous sessions reopen with the last conversations

## Prerequisites
- Node.js 18 or newer (the Vite toolchain requires modern Node features)
- The chatbot API reachable at `http://localhost:8002` with the `/api/message/add` and `/api/message/rate` endpoints

## Install Dependencies
```bash
npm install
```

## Run in Development
```bash
npm run dev
```
Vite prints a local URL (default `http://localhost:5173`). Open it in the browser. Start the backend first so messages get real responses.



## Backend Server (FastAPI)
The UI expects the FastAPI backend that lives in `../Server`.

1. Ensure Python 3.10+ is installed.
2. (Optional) create and activate a virtual environment:
   ```bash
   cd ../Server
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Review `config.json` to confirm the host/port (`8002` by default) and the remote LLM/search endpoints. Adjust them if your environment differs.
5. Start the API:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8002
   ```
   For production drop the `--reload` flag or run `python app/main.py`.
6. The UI calls:
   - `POST /api/message/add` for sending prompts
   - `POST /api/message/rate` for feedback
   Make sure these endpoints respond before launching the frontend.


