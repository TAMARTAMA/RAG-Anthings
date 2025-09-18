# pip install -U trl transformers datasets accelerate peft bitsandbytes

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from trl import DPOTrainer, DPOConfig
from peft import LoraConfig

BASE_MODEL = "Qwen/Qwen2-0.5B-Instruct"  # אפשר גם Qwen/Qwen2.5-0.5B-Instruct
DATA_PATH = {
    "train": "data/hh-rlhf/train/train.pairwise.jsonl",
    "eval":  "data/hh-rlhf/test/test.pairwise.jsonl",
}

# 1) טוענים Tokenizer ומודל
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, use_fast=True, trust_remote_code=True)
# לרוב אין pad_token; נשתמש ב-eos כ-PAD
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# טעינת מודל עם 8-bit/4-bit להקטנת זיכרון (אופציונלי)
model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    torch_dtype="auto",
    device_map="auto",
    trust_remote_code=True,
    load_in_8bit=True,  # או load_in_4bit=True אם מותקן bitsandbytes תואם
)

# 2) דאטה בפורמט DPO: עמודות ['prompt','chosen','rejected']
ds_train = load_dataset("json", data_files={"train": DATA_PATH["train"]})["train"]
ds_eval  = load_dataset("json", data_files={"eval":  DATA_PATH["eval"]})["eval"]

# 3) הגדרות LoRA (קטן וזול)
peft_config = LoraConfig(
    r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"],  # נפוץ ב-Qwen
    task_type="CAUSAL_LM",
)

# 4) קונפיג DPO
dpo_config = DPOConfig(
    output_dir="outputs/qwen2-0_5b-dpo",
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=5e-5,
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=200,
    save_steps=200,
    num_train_epochs=1,            # התחלתי; אפשר לעדכן
    max_length=1024,               # אורך רצף כולל prompt+response
    max_target_length=512,         # אורך התשובה
    warmup_ratio=0.05,
)

# 5) מאמן DPO
trainer = DPOTrainer(
    model=model,
    tokenizer=tokenizer,
    args=dpo_config,
    train_dataset=ds_train,
    eval_dataset=ds_eval,
    peft_config=peft_config,       # LoRA
    formatting_func=None,          # אפשר להשאיר, אם השדות כבר בפורמט prompt/chosen/rejected
    padding_value=tokenizer.pad_token_id,
)

trainer.train()
trainer.save_model()        # ישמור אדפטרים אם LoRA; אחרת מודל מלא
tokenizer.save_pretrained(dpo_config.output_dir)
