#!/usr/bin/env bash
set -euo pipefail

# === CONFIG ===
PROJECT_ROOT="/home/ext-z/Moptimizer/task_1_UI/model"
VENV_DIR="$PROJECT_ROOT/venv"

# Choices: "cpu" or a specific CUDA tag like "cu121" (CUDA 12.1)
# Default is CPU-only to keep it simple.
TORCH_FLAVOR="${TORCH_FLAVOR:-cpu}"

echo ">>> Using PROJECT_ROOT=$PROJECT_ROOT"
echo ">>> Creating venv at $VENV_DIR"

mkdir -p "$PROJECT_ROOT"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

python -m pip install --upgrade pip wheel setuptools

echo ">>> Installing python requirements (without torch)"
pip install -r "$PROJECT_ROOT/requirements.txt"

echo ">>> Installing PyTorch ($TORCH_FLAVOR)"
if [[ "$TORCH_FLAVOR" == "cpu" ]]; then
  pip install torch --index-url https://download.pytorch.org/whl/cpu
else
  # Example: TORCH_FLAVOR=cu121 for CUDA 12.1
  pip install torch --index-url "https://download.pytorch.org/whl/${TORCH_FLAVOR}"
fi

echo ">>> Done."
echo
echo "To run the server:"
echo "  source "$VENV_DIR/bin/activate""
echo "  python "$PROJECT_ROOT/modelruning.py""
echo
echo "If your sample.py is in a different folder, set ROOT in modelruning.py or via env."
