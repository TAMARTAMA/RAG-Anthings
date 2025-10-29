## Transcription API
=================

FastAPI server for speech-to-text transcription using OpenAI Whisper.

# Setup
-----
pip install fastapi uvicorn openai-whisper torch torchvision torchaudio 

# Run
---
uvicorn server:app --host 0.0.0.0 --port 8000

# Usage
-----
curl -X POST "http://localhost:8000/transcribe" \
  -F "file=@sample.wav" \
  -F "language=auto"

# Response:
{"text": "Hello world", "language": "en"}

# Notes
-----
- Temporary files are auto-deleted.
- CORS allows requests from http://localhost:5173
- Model size can be changed in config.py by editing:
  MODEL_NAME = "base"
  (options: tiny, base, small, medium, large)
