from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, Gemma3ForConditionalGeneration
from pathlib import Path
import torch, json, time

# ===== Load Config =====
CFG_PATH = Path(__file__).with_name("config.json")
cfg = json.loads(CFG_PATH.read_text(encoding="utf-8"))

MODEL_DIR = cfg["model_dir"]
DTYPE = torch.bfloat16
DEVICE_MAP = cfg.get("device_map")

# ===== FastAPI Init =====
app = FastAPI(title="LLM Server (Gemma 3 4B IT)")
_model = None
_tok = None

class GenerateIn(BaseModel):
    messages: list[dict]
    max_new_tokens: int = cfg.get("default_max_new_tokens", 1024)
    temperature: float = cfg.get("default_temperature", 0.0)

class GenerateOut(BaseModel):
    text: str
    tokens: int
    duration_s: float

# --- Schemas for /probabilities ---
class ProbabilitiesIn(BaseModel):
    messages: list[dict]
    temperature: float = 1.0

class TokenProb(BaseModel):
    token: str
    prob: float

class ProbabilitiesOut(BaseModel):
    items: list[TokenProb]


@app.on_event("startup")
def load_model():
    global _model, _tok
    print(f"[LOAD] Loading model from {MODEL_DIR} ...", end="", flush=True)
    _model = Gemma3ForConditionalGeneration.from_pretrained(
        MODEL_DIR, local_files_only=True, device_map=DEVICE_MAP, dtype=DTYPE
    ).eval()
    _tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    print(" done.")

@app.get("/health")
def health():
    return {"ok": _model is not None, "model": MODEL_DIR}

@app.post("/generate", response_model=GenerateOut)
def generate(req: GenerateIn):
    # basic validation
    if not isinstance(req.messages, list) or len(req.messages) == 0:
        raise HTTPException(status_code=400, detail="messages must be a non-empty list")

    start = time.time()

    # chat template -> tensor
    inputs = _tok.apply_chat_template(
        req.messages, add_generation_prompt=True, return_tensors="pt"
    ).to(_model.device)

    with torch.inference_mode():
        out = _model.generate(
            input_ids=inputs,
            max_new_tokens=req.max_new_tokens,
            temperature=req.temperature,
        )

    gen_ids = out[0][inputs.shape[-1]:]
    text = _tok.decode(gen_ids, skip_special_tokens=True).strip()
    dur = time.time() - start
    return GenerateOut(text=text, tokens=gen_ids.numel(), duration_s=dur)

# --- Endpoint: full next-token distribution as [{token, prob}] ---
@app.post("/probabilities", response_model=ProbabilitiesOut)
def probabilities(req: ProbabilitiesIn):
    if not isinstance(req.messages, list) or len(req.messages) == 0:
        raise HTTPException(status_code=400, detail="messages must be a non-empty list")

    # Build model inputs using the same chat template as /generate
    inputs = _tok.apply_chat_template(
        req.messages, add_generation_prompt=True, return_tensors="pt"
    ).to(_model.device)

    # Temperature safeguard (avoid division by zero)
    t = max(1e-6, float(req.temperature))

    with torch.inference_mode():
        logits = _model(input_ids=inputs).logits[:, -1, :]   # [1, vocab_size]
        probs = torch.softmax(logits / t, dim=-1)[0]         # [vocab_size]

    V = probs.shape[0]
    ids = list(range(V))

    # Try direct ID->token conversion; may produce None/"" for some IDs
    tokens = _tok.convert_ids_to_tokens(ids)

    # Fill any missing/empty entries via decode; if still empty -> "<id:N>"
    for i, tok in enumerate(tokens):
        if tok is None or tok == "":
            fallback = _tok.decode([i], skip_special_tokens=False)
            tokens[i] = fallback if fallback not in (None, "") else f"<id:{i}>"

    items = [{"token": tokens[i], "prob": float(probs[i])} for i in range(V)]
    return ProbabilitiesOut(items=items)