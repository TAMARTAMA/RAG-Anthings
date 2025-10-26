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

## Build for Production
```bash
npm run build
```
The optimized output lives in `dist/`. To preview the production bundle locally run:
```bash
npm run preview
```

## Linting
```bash
npm run lint
```

## Troubleshooting
- If chat requests fail, confirm the backend is listening on port 8002 and that CORS allows the frontend origin.
- Delete the browser's local storage (key `chatHistory`) if you want to reset saved conversations.
