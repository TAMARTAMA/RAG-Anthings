import pandas as pd


pairs = pd.read_parquet("data/hh-rlhf/train/train.parquet")

flat = pd.read_parquet("data/hh-rlhf/train/train.flat.parquet")
print(flat.head())