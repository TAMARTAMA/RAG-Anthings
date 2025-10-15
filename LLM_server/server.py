from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, Gemma3ForConditionalGeneration
from pathlib import Path
import torch, json, time

# ===== Load Config =====
CFG_PATH = Path(__file__).with_name("config.json")
cfg = json.loads(CFG_PATH.read_text(encoding="utf-8"))

MODEL_DIR = cfg["model_dir"]
DTYPE = {"float32": torch.float32, "bfloat16": torch.bfloat16}.get(cfg.get("dtype", "float32"), torch.float32)
DEVICE_MAP = cfg.get("device_map", "cpu")
SYSTEM_PROMPT = cfg.get("system_prompt", "You are a helpful assistant.")

# ===== FastAPI Init =====
app = FastAPI(title="LLM Server (Gemma 3 4B IT)")
_model = None
_tok = None

class GenerateIn(BaseModel):
    prompt: str
    max_new_tokens: int = cfg.get("default_max_new_tokens", 200)
    temperature: float = cfg.get("default_temperature", 0.2)
    top_p: float = cfg.get("default_top_p", 1.0)
    do_sample: bool = cfg.get("default_do_sample", False)

class GenerateOut(BaseModel):
    text: str
    tokens: int
    duration_ms: int

@app.on_event("startup")
def load_model():
    global _model, _tok
    print(f"[LOAD] Loading model from {MODEL_DIR} ...")
    _model = Gemma3ForConditionalGeneration.from_pretrained(
        MODEL_DIR, local_files_only=True, device_map=DEVICE_MAP, dtype=DTYPE
    ).eval()
    _tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    print("[READY] Model loaded successfully.")

@app.get("/health")
def health():
    return {"ok": _model is not None, "model": MODEL_DIR}

@app.post("/generate", response_model=GenerateOut)
def generate(req: GenerateIn):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Empty prompt")

    start = time.time()
    messages = [
        {"role": "system", "content": [{"type": "text", "text": SYSTEM_PROMPT}]},
        {"role": "user", "content": [{"type": "text", "text": req.prompt}]},
    ]

    inputs = _tok.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(_model.device)
    with torch.inference_mode():
        out = _model.generate(
            input_ids=inputs,
            attention_mask=(inputs != _tok.pad_token_id).long() if _tok.pad_token_id else None,
            max_new_tokens=req.max_new_tokens,
            temperature=req.temperature,
            top_p=req.top_p,
            do_sample=req.do_sample,
        )

    gen_ids = out[0][inputs.shape[-1]:]
    text = _tok.decode(gen_ids, skip_special_tokens=True).strip()
    dur = int((time.time() - start) * 1000)
    return GenerateOut(text=text, tokens=gen_ids.numel(), duration_ms=dur)

# run:

# uvicorn Moptimizer.LLM_server.server:app --host 0.0.0.0 --port 8013

# another terminal:
# curl -s http://127.0.0.1:8013/health
# curl -s -X POST http://127.0.0.1:8013/generate -H 'Content-Type: application/json' \
#   -d '{"prompt":"Say hi in one word","max_new_tokens":4,"temperature":0.0}'
