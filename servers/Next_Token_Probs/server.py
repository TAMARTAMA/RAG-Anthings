import json
from pathlib import Path
from typing import List, Dict, Any

import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, Gemma3ForConditionalGeneration


# ========= Load config =========
CFG_PATH = Path(__file__).with_name("config.json")
cfg = json.loads(CFG_PATH.read_text(encoding="utf-8"))

MODEL_DIR = str(Path(cfg["model_dir"]))            # local model directory
DTYPE_STR = cfg.get("dtype", "float32")            # "float32" | "bfloat16"
DEFAULT_TOP_K = int(cfg.get("default_top_k", 20))

DTYPE = {"float32": torch.float32, "bfloat16": torch.bfloat16}.get(DTYPE_STR, torch.float32)


# ========= Initialize model/tokenizer once at startup =========
# Note: local_files_only=True ensures no network is used.
model = Gemma3ForConditionalGeneration.from_pretrained(
    MODEL_DIR, local_files_only=True, device_map="cpu", dtype=DTYPE
).eval()
tok = AutoTokenizer.from_pretrained(MODEL_DIR)

app = FastAPI(title="Gemma Next-Token Probs", version="1.0")


# ========= Request/Response schemas =========
class NextTokenRequest(BaseModel):
    question: str
    top_k: int | None = None  # if omitted, DEFAULT_TOP_K is used


class TopToken(BaseModel):
    token_id: int
    token: str
    prob: float


class NextTokenResponse(BaseModel):
    top_k: List[TopToken]
    vocab_size: int


# ========= Helper: build chat-style messages =========
def build_messages(question: str) -> list[dict[str, Any]]:
    """
    Build the conversation messages Gemma-3 expects.
    """
    return [
        {"role": "system", "content": [{"type": "text", "text": "You are a helpful and concise assistant."}]},
        {"role": "user",   "content": [{"type": "text", "text": question}]},
    ]


# ========= Core: compute next-token distribution and return top-k =========
def next_token_topk(question: str, k: int) -> Dict[str, Any]:
    """
    Returns the top-k next-token probabilities and the vocabulary size.
    """
    messages = build_messages(question)

    # Convert chat messages to token IDs using the model's chat template.
    input_ids = tok.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")

    with torch.inference_mode():
        # Forward pass (no generation): get logits for all positions.
        out = model(input_ids=input_ids)                 # logits shape: [batch, seq_len, vocab_size]
        next_logits = out.logits[:, -1, :]               # last position => next-token logits
        probs = torch.softmax(next_logits, dim=-1)       # convert logits to probabilities

    # Select top-k tokens.
    vocab_size = int(probs.shape[-1])                    # true vocabulary size
    k = max(1, min(k, vocab_size))
    top_p, top_i = torch.topk(probs, k=k, dim=-1)

    items: List[Dict[str, Any]] = []
    for p, i in zip(top_p[0], top_i[0]):
        token_id = int(i)
        token_text = tok.decode(i.unsqueeze(0))          # decode the single token for readability
        items.append({"token_id": token_id, "token": token_text, "prob": float(p)})

    return {"top_k": items, "vocab_size": vocab_size}


# ========= API route =========
@app.post("/next_token_probs", response_model=NextTokenResponse)
def api_next_token_probs(body: NextTokenRequest):
    """
    Input:  JSON with 'question' and optional 'top_k'.
    Output: JSON with a 'top_k' list of tokens and probabilities, and 'vocab_size'.
    """
    k = body.top_k or DEFAULT_TOP_K
    return next_token_topk(body.question, k)

# ==run=========

# uvicorn server:app --host 0.0.0.0 --port 8000 --reload

# curl -X POST "http://127.0.0.1:8000/next_token_probs" \
#   -H "Content-Type: application/json" \
#   -d '{"question":"Give a one-line summary of BPE.","top_k": 10}'
