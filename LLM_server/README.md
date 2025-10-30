# Gemma 3 LLM Server

## Overview
A lightweight FastAPI server that loads a local Gemma 3 model and exposes endpoints:
- **/health** – basic health check  
- **/generate** – text generation based on chat messages  
- **/probabilities** – full next-token probability distribution (returns `[{ token, prob }]`)  

Includes basic unit tests and a stress test script for performance evaluation.

---

## Directory Structure
```
Moptimizer/
└── LLM_server/
    ├── __init__.py                 # marks package for imports in tests
    ├── server.py                   # FastAPI server
    ├── config.json                 # Model configuration file
    ├── test_generate.py            # Unit tests for /generate
    ├── test_probabilities.py       # Unit tests for /probabilities
    ├── stress_test_generate.py     # Stress/load testing script
```

---

## Running the Server
1. Verify `config.json` contains a valid local model path.
2. Start the server:
   ```bash
   uvicorn Moptimizer.LLM_server.server:app --host 0.0.0.0 --port 8013
   ```
3. Example requests:
   - **/generate**
     ```bash
     curl -s -X POST http://127.0.0.1:8013/generate \
       -H 'Content-Type: application/json' \
       -d '{
             "messages": [
               { "role": "user", "content": [ { "type": "text", "text": "Say hi in one word." } ] }
             ],
             "max_new_tokens": 8,
             "temperature": 0.0001
           }'
     ```
   - **/probabilities**
     ```bash
     curl -s -X POST http://127.0.0.1:8013/probabilities \
       -H 'Content-Type: application/json' \
       -d '{
             "messages": [
               { "role": "user", "content": [ { "type": "text", "text": "Say hi in one word." } ] }
             ]
           }'
     ```

---

## Running the Tests
Run unit tests (without starting the server):
```bash
PYTHONPATH=. pytest -q Moptimizer/LLM_server/test_generate.py Moptimizer/LLM_server/test_probabilities.py
```

Run performance test (server must be running):
```bash
python Moptimizer/LLM_server/stress_test_generate.py \
  --url http://127.0.0.1:8013/generate --rate 50 --seconds 10
```
