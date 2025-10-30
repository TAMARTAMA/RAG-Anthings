# Transcription API


FastAPI server for speech-to-text transcription using OpenAI Whisper.

## Setup

pip install fastapi uvicorn openai-whisper torch torchvision torchaudio python-multipart 

## Run

uvicorn server:app --host 0.0.0.0 --port 8000

## Usage

curl -X POST "http://localhost:8000/transcribe" \
  -F "file=@sample.mp3" \
  -F "language=auto"


## Response:
{"text": "Hello world", "language": "en"}

## Notes

- Temporary files are auto-deleted.
- CORS allows requests from http://localhost:5173
- Model size can be changed in config.py by editing:
  MODEL_NAME = "base"
  (options: tiny, base, small, medium, large, turbo)
## Available Models and Requirements
| Model Size | Parameters | English-only Model | Multilingual Model | Required VRAM | Relative Speed* |
| ---------- | ---------- | ------------------ | ------------------ | ------------- | --------------- |
| **tiny**   | 39 M       | `tiny.en`          | `tiny`             | ~1 GB         | ~10× faster     |
| **base**   | 74 M       | `base.en`          | `base`             | ~1 GB         | ~7× faster      |
| **small**  | 244 M      | `small.en`         | `small`            | ~2 GB         | ~4× faster      |
| **medium** | 769 M      | `medium.en`        | `medium`           | ~5 GB         | ~2× faster      |
| **large**  | 1550 M     | N/A                | `large`            | ~10 GB        | 1× (reference)  |
| **turbo**  | 809 M      | N/A                | `turbo`            | ~6 GB         | ~8× faster      |

*Relative speed measured on an NVIDIA A100 GPU with English speech input.
Real-world performance may vary depending on hardware, language, and audio length.

## Performance Notes

- The turbo model is optimized for speed — it runs significantly faster than base, with only a minimal trade-off in accuracy.

- English-only models (.en) generally perform better on English audio, especially for the tiny.en and base.en models.

- For small and larger models, the accuracy difference between English-only and multilingual versions becomes negligible.
