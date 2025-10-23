# One-shot Setup & Run

This repo uses a Python virtual environment (venv) so system Python stays clean (PEP 668).

## Files
- `requirements.txt` – common Python deps except PyTorch
- `install.sh` – creates a venv and installs all deps including PyTorch (CPU by default)
- `modelruning.py` – your FastAPI server (already prepared)

Paths used in scripts:
- Project root for the model server: `/home/ext-z/Moptimizer/task_1_UI/model`
- nanoGPT tree: `/home/ext-z/nanoGPT/Moptimizer/nanoGPT`
- ckpt: `/home/ext-z/nanoGPT/Moptimizer/nanoGPT/runs/exp003 - more data/ckpt.pt`

## Install (CPU-only default)
```bash
cd /home/ext-z/Moptimizer/task_1_UI/model
# Put requirements.txt and install.sh in this folder
bash install.sh
```

This will:
1. Create a virtualenv at `/home/ext-z/Moptimizer/task_1_UI/model/venv`
2. Install packages from `requirements.txt`
3. Install PyTorch (CPU wheel)

## Install with CUDA
If you have NVIDIA drivers/CUDA and want GPU acceleration:
```bash
cd /home/ext-z/Moptimizer/task_1_UI/model
TORCH_FLAVOR=cu121 bash install.sh   # CUDA 12.1 example
```
Other tags (e.g., `cu118`) are available at https://pytorch.org/get-started/locally/

## Run the server
```bash
cd /home/ext-z/Moptimizer/task_1_UI/model
source venv/bin/activate
python modelruning.py
```
Test:
```bash
curl -X POST http://127.0.0.1:8001/generate   -H "Content-Type: application/json"   -d '{"prompt":"בבקשה השלם לי את המשפט: התקנון נועד לשם ","num_samples":1,"max_new_tokens":80,"temperature":0.6,"top_k":200}'
```

## Node side
Set MODEL_URL and run your API:
```bash
export MODEL_URL="http://127.0.0.1:8001/generate"
# restart your Node server so it picks up the env var
```

## Troubleshooting
- `ModuleNotFoundError: torch` → rerun `bash install.sh` (ensures PyTorch is installed in venv).
- `ModuleNotFoundError: tiktoken` → `source venv/bin/activate && pip install tiktoken`.
- `externally-managed-environment` → Always use the venv created by `install.sh`.
