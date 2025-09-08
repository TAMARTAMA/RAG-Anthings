# rlhf_data_fallback.py
# pip install -U datasets pyarrow pandas

import os
import json
from pathlib import Path
from typing import Dict, Any, Iterable

import pandas as pd
from datasets import load_dataset, Dataset, DatasetDict

OUT_DIR = Path("data/hh-rlhf")
LOCAL_DIR = Path("local_hh_rlhf")  # שימי כאן את train.jsonl.gz / test.jsonl.gz אם הורדת מקומית

def to_jsonl(path: Path, rows: Iterable[Dict[str, Any]]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def try_load_remote() -> DatasetDict | None:
    try:
        print("Trying to load remote dataset: Anthropic/hh-rlhf ...")
        ds = load_dataset("Anthropic/hh-rlhf")
        print("Loaded remote successfully.")
        return ds
    except Exception as e:
        print(f"[INFO] Remote load failed: {e.__class__.__name__}: {e}")
        return None

def try_load_local() -> DatasetDict | None:
    train_path = LOCAL_DIR / "train.jsonl.gz"
    test_path = LOCAL_DIR / "test.jsonl.gz"
    data_files = {}
    if train_path.exists():
        data_files["train"] = str(train_path)
    if test_path.exists():
        data_files["test"] = str(test_path)
    if not data_files:
        return None
    print(f"Loading local JSONL files from {LOCAL_DIR} ...")
    ds = load_dataset("json", data_files=data_files, split=None)
    print("Loaded local successfully.")
    return ds

def build_toy_dataset() -> DatasetDict:
    print("[WARN] No remote/local dataset available. Building a tiny toy dataset...")
    toy_train = [
        {"prompt": "Write a short greeting.", "chosen": "Hello! Great to meet you.", "rejected": "No."},
        {"prompt": "Summarize: RLHF improves alignment.", "chosen": "RLHF helps models follow instructions better.",
         "rejected": "I like pizza."},
    ]
    toy_test = [
        {"prompt": "Give a tip for studying.", "chosen": "Practice daily and review mistakes.",
         "rejected": "Stop learning."}
    ]
    # נשמור ל-local כדי שגם הריצות הבאות יעבדו
    LOCAL_DIR.mkdir(parents=True, exist_ok=True)
    to_jsonl(LOCAL_DIR / "train.jsonl", toy_train)
    to_jsonl(LOCAL_DIR / "test.jsonl", toy_test)
    ds = load_dataset("json",
                      data_files={
                          "train": str(LOCAL_DIR / "train.jsonl"),
                          "test": str(LOCAL_DIR / "test.jsonl"),
                      })
    return ds

def build_pairwise_row(row: Dict[str, Any]) -> Dict[str, Any]:
    prompt = row.get("prompt", "")
    return {
        "prompt": prompt if prompt is not None else "",
        "chosen": row["chosen"],
        "rejected": row["rejected"],
    }

def main():
    # 1) ניסוי רשת → 2) מקומי → 3) דאטה זעיר
    ds = try_load_remote()
    if ds is None:
        ds = try_load_local()
    if ds is None:
        ds = build_toy_dataset()

    print(ds)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # הדפסה קצרה ודוגמאות
    for split_name, split in ds.items():
        print(f"\n=== {split_name} ===")
        print(split)
        print("Columns:", split.column_names)
        print("Example:", {k: split[0][k] for k in split.column_names})

    # שמירה Parquet + JSONL גולמי
    for split_name, split in ds.items():
        split_dir = OUT_DIR / split_name
        split_dir.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame(split.to_dict())
        df.to_parquet(split_dir / f"{split_name}.parquet", index=False)

        to_jsonl(split_dir / f"{split_name}.jsonl", (split[i] for i in range(len(split))))
        print(f"Saved {split_dir / f'{split_name}.parquet'}")
        print(f"Saved {split_dir / f'{split_name}.jsonl'}")

    # יצירת גרסת pairwise
    for split_name, split in ds.items():
        pairwise_rows = (build_pairwise_row(split[i]) for i in range(len(split)))
        to_jsonl(OUT_DIR / split_name / f"{split_name}.pairwise.jsonl", pairwise_rows)
        print(f"Saved {OUT_DIR / split_name / f'{split_name}.pairwise.jsonl'}")

    # גרסת like/dislike שטוחה
    for split_name, split in ds.items():
        flat_rows = []
        for i in range(len(split)):
            row = split[i]
            prompt = row.get("prompt", "") or ""
            flat_rows.append({"prompt": prompt, "response": row["chosen"], "label": 1})
            flat_rows.append({"prompt": prompt, "response": row["rejected"], "label": 0})
        flat_df = pd.DataFrame(flat_rows)
        split_dir = OUT_DIR / split_name
        flat_df.to_parquet(split_dir / f"{split_name}.flat.parquet", index=False)
        to_jsonl(split_dir / f"{split_name}.flat.jsonl", flat_rows)
        print(f"Saved {split_dir / f'{split_name}.flat.parquet'}")
        print(f"Saved {split_dir / f'{split_name}.flat.jsonl'}")

    print("\nDone. Files are under:", OUT_DIR.resolve())

if __name__ == "__main__":
    main()
