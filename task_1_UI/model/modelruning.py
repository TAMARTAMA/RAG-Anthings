
# /home/ext-z/Moptimizer/task_1_UI/model/modelruning.py
# FastAPI server for nanoGPT sampling via sample.py
# - Uses temporary config file for configurator
# - Forces CPU
# - Cleans sample.py stdout so API returns only the generated text (without logs)
#
# Run:
#   source /home/ext-z/Moptimizer/task_1_UI/model/venv/bin/activate
#   python /home/ext-z/Moptimizer/task_1_UI/model/modelruning.py

import os
import sys
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# -----------------------------
# Fixed paths per your setup
# -----------------------------
ROOT = Path("/home/ext-z/nanoGPT/Moptimizer/nanoGPT")
OUT_DIR = Path("/home/ext-z/nanoGPT/Moptimizer/nanoGPT/runs/exp003 - more data")

# Force CPU environment and expose ckpt path (if sample.py uses it)
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ.setdefault("CKPT_PATH", str(OUT_DIR / "ckpt.pt"))

PYTHON = sys.executable

# -----------------------------
# Utils
# -----------------------------
def _py_literal(val):
    if isinstance(val, str):
        return "'" + val.replace("'", "\\'") + "'"
    if val is None:
        return "None"
    return str(val)

def _write_config_file(*, out_dir: str, start: str,
                       max_new_tokens: int, temperature: float,
                       top_k: Optional[int], seed: Optional[int]) -> Path:
    lines = [
        f"out_dir = {_py_literal(out_dir)}",
        f"device = 'cpu'",
        f"start = {_py_literal(start)}",
        f"max_new_tokens = {max_new_tokens}",
        f"temperature = {temperature}",
    ]
    if top_k is not None:
        lines.append(f"top_k = {top_k}")
    if seed is not None:
        lines.append(f"seed = {seed}")
    cfg_text = "\n".join(lines) + "\n"

    tmp = tempfile.NamedTemporaryFile('w', suffix='.py', delete=False, encoding='utf-8')
    tmp.write(cfg_text)
    tmp.flush()
    tmp.close()
    return Path(tmp.name)

def _clean_generation(stdout_text: str) -> str:
    """
    Strip logs and return only the generated text.
    Heuristics:
      - Drop everything up to and including the last 'Loading meta' line (if present).
      - Then take only the first block before '---------------' (if present).
      - Trim whitespace.
    """
    lines = stdout_text.splitlines()
    start_idx = 0
    for i, line in enumerate(lines):
        if "Loading meta" in line:
            start_idx = i + 1
    gen = "\n".join(lines[start_idx:]).strip()

    # Remove common preface log lines if any survived
    prefaces = (
        "Overriding config with",
        "number of parameters:",
        "UserWarning:",
    )
    cleaned_lines = []
    for ln in gen.splitlines():
        if any(ln.startswith(p) for p in prefaces):
            continue
        cleaned_lines.append(ln)
    gen = "\n".join(cleaned_lines).strip()

    # Take only first block before dashed separator, if exists
    if "---------------" in gen:
        gen = gen.split("---------------", 1)[0].strip()

    return gen

# -----------------------------
# Samplers
# -----------------------------
def sample_once(prompt: str,
                *,
                max_new_tokens: int = 100,
                temperature: float = 0.7,
                top_k: Optional[int] = None,
                seed: Optional[int] = None) -> str:
    ROOT.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    cfg_path = _write_config_file(
        out_dir=str(OUT_DIR),
        start=prompt,
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        top_k=top_k,
        seed=seed,
    )

    args = [PYTHON, "-X", "utf8", "sample.py", str(cfg_path)]
    try:
        out = subprocess.check_output(args, cwd=str(ROOT), stderr=subprocess.STDOUT, timeout=300)
        raw = out.decode("utf-8", errors="replace")
        return _clean_generation(raw)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(e.output.decode("utf-8", errors="replace")) from e
    except subprocess.TimeoutExpired as e:
        raise RuntimeError("sample.py timed out") from e
    finally:
        try:
            os.unlink(cfg_path)
        except Exception:
            pass

def sample_n(prompt: str,
             *,
             num_samples: int = 1,
             max_new_tokens: int = 100,
             temperature: float = 0.7,
             top_k: Optional[int] = None,
             seed: Optional[int] = 0,
             seed_increment: bool = True) -> list[dict]:
    samples = []
    current_seed = seed
    for i in range(num_samples):
        text = sample_once(
            prompt=prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_k=top_k,
            seed=current_seed,
        )
        samples.append({"index": i, "seed": current_seed, "text": text})
        if seed_increment and current_seed is not None:
            current_seed += 1
    return samples

# -----------------------------
# FastAPI
# -----------------------------
app = FastAPI(title="Text Generation Server", version="1.0")

class GenerateRequest(BaseModel):
    prompt: str
    num_samples: int = 1
    max_new_tokens: int = 128
    temperature: float = 0.7
    top_k: Optional[int] = 200
    seed: Optional[int] = 0
    seed_increment: bool = True

class GenerateResponse(BaseModel):
    completions: List[str]

@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    try:
        samples = sample_n(
            prompt=req.prompt,
            num_samples=req.num_samples,
            max_new_tokens=req.max_new_tokens,
            temperature=req.temperature,
            top_k=req.top_k,
            seed=req.seed,
            seed_increment=req.seed_increment
        )
        texts = [s.get("text", "").strip() for s in samples]
        if not any(texts):
            raise ValueError("Model returned no text")
        return GenerateResponse(completions=texts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("modelruning:app", host="0.0.0.0", port=8001)
