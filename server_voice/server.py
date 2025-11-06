from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import whisper, tempfile, os
from config import MODEL_NAME, DEVICE
import time

# Load Whisper model
model = whisper.load_model(MODEL_NAME, device=DEVICE)

# Init FastAPI app
app = FastAPI(title="Transcription API")


# Define allowed origins for both dev and production
allowed_origins = [
    "http://localhost:5173",          # Local development
    "http://127.0.0.1:5173",          # Alternate local access
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST", "OPTIONS"],   # Limit to only what’s needed
    allow_headers=["Content-Type", "Authorization"],  # Limit allowed headers
)


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...), language: str = Form("auto")):
    """Transcribe uploaded audio using Whisper."""
    ext = os.path.splitext(file.filename)[1] or ".webm"
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        data = await file.read()
        tmp.write(data)
        path = tmp.name

    try:
        print(f"[*] Received file: {file.filename}, size: {len(data)} bytes")
        
        # Measure transcription time
        start_time = time.time()
        result = model.transcribe(path, language=None if language == "auto" else language)
        end_time = time.time()

        duration = end_time - start_time
        print(f"[*] Transcription completed in {duration:.2f} seconds")
        return JSONResponse({
            "text": result["text"].strip(),
            "language": result.get("language", "unknown")
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        os.remove(path)


