from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM, Gemma3ForConditionalGeneration, BitsAndBytesConfig
from pathlib import Path
import torch, json, time

# ===== Load Config =====
CFG_PATH = Path(__file__).with_name("config.json")
cfg = json.loads(CFG_PATH.read_text(encoding="utf-8"))

MODEL_DIR = cfg["model_dir"]
DEVICE_MAP = cfg.get("device_map", "auto")

quant_mode = cfg.get("quantization", "none")  # "none" / "int8"

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
    prompt: str

class TokenProb(BaseModel):
    token: str
    prob: float

class ProbabilitiesOut(BaseModel):
    items: list[TokenProb]


@app.on_event("startup")
def load_model():
    global _model, _tok
    print(f"[LOAD] Loading model from {MODEL_DIR} (quant={quant_mode})...", end="", flush=True)

    if quant_mode == "int8":
        # === INT8 MODE ===
        quant_cfg = BitsAndBytesConfig(load_in_8bit=True)
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_DIR,
            quantization_config=quant_cfg,
            torch_dtype=torch.bfloat16,   
            device_map=DEVICE_MAP,         
            local_files_only=True
        ).eval()
    else:
        # === BF16 ===
        _model = AutoModelForCausalLM.from_pretrained(
            MODEL_DIR,
            device_map=DEVICE_MAP,
            dtype=torch.bfloat16,
            local_files_only=True
        ).eval()

    _tok = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
    if _tok.pad_token_id is None and _tok.eos_token_id is not None:
        _tok.pad_token = _tok.eos_token
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
    if not isinstance(req.prompt, str) or not req.prompt.strip():
        raise HTTPException(status_code=400, detail="prompt must be a non-empty string")

    inputs = _tok.apply_chat_template(
        [{"role": "user", "content": req.prompt}],
        add_generation_prompt=True,          
        return_tensors="pt"
    ).to(_model.device)

    with torch.inference_mode():
        logits = _model(input_ids=inputs).logits[:, -1, :]  
        probs = torch.softmax(logits.to(torch.float32), dim=-1)[0]
        probs = probs / probs.sum()

    V = probs.shape[0]
    ids = list(range(V))
    tokens = _tok.convert_ids_to_tokens(ids)
    for i, tok in enumerate(tokens):
        if tok is None or tok == "":
            fallback = _tok.decode([i], skip_special_tokens=False)
            tokens[i] = fallback if fallback not in (None, "") else f"<id:{i}>"

    items = [{"token": tokens[i], "prob": float(probs[i])} for i in range(V)]
    return ProbabilitiesOut(items=items)
