import pandas as pd

# טבלת pairwise (ל-RLHF)
pairs = pd.read_parquet("data/hh-rlhf/train/train.parquet")
# או גרסת זוגות המפורשת:
# pairs_jsonl = "data/hh-rlhf/train/train.pairwise.jsonl"

# גרסת like/dislike שטוחה (למודל תגמול/מסווג)
flat = pd.read_parquet("data/hh-rlhf/train/train.flat.parquet")
print(flat.head())