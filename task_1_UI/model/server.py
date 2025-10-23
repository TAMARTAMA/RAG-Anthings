from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess, sys, os

app = FastAPI(title="Model Inference API")

class InferRequest(BaseModel):
    prompt: str
    timeout_sec: int = 60

def _run_model_script(prompt: str, timeout_sec: int = 60) -> str:
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "modelruning.py"))
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"modelruning.py not found at: {script_path}")
    cmd = [sys.executable, script_path, prompt]
    try:
        res = subprocess.run(cmd, capture_output=True, timeout=timeout_sec, text=True)
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"Timed out after {timeout_sec}s waiting for model response")
    if res.returncode != 0:
        stderr = (res.stderr or "").strip()
        raise RuntimeError(f"modelruning.py failed (exit {res.returncode}): {stderr}")
    return (res.stdout or "").strip()

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/generate")
def generate(req: InferRequest):
    try:
        text = _run_model_script(req.prompt, req.timeout_sec)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"text": text}
