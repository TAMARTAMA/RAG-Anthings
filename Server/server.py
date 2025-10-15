
from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import os, time, json
import uuid, hashlib


from transformers import pipeline
# try:
#     from transformers import pipeline
# except Exception:
#     pipeline = None

from pydantic import BaseModel

class Ask(BaseModel):
    message: str   


class ModelService:
    def __init__(self, model_dir: str, max_new_tokens: int = 64, do_sample: bool = False):
        p = Path(model_dir)
        self.max_new_tokens = int(max_new_tokens)
        self.do_sample = bool(do_sample)
        self.pipe = pipeline("text-generation", model=str(p)) if pipeline and p.exists() else None
    def infer(self, prompt: str) -> str:
        if self.pipe:
            out = self.pipe(
                prompt,
                max_new_tokens=self.max_new_tokens,
                do_sample=self.do_sample,
            )[0]["generated_text"]
            return (out[len(prompt):] or out).strip()
        return f"echo: {prompt}"
    
class RateRequest(BaseModel):
    id_question: int      
    rating: int          
app = FastAPI()

_CONFIG_PATH = Path(__file__).resolve().parent / "config.json"
_cfg = {
    "model_dir": "./Model",
    "chat_dir": "./Chats",
    "server": {"host": "0.0.0.0", "port": 8000},
    "generation": {"max_new_tokens": 64, "do_sample": False},
}
if _CONFIG_PATH.exists():
    try:
        _cfg.update(json.loads(_CONFIG_PATH.read_text(encoding="utf-8")))
    except Exception:
        pass

MODEL_DIR = os.getenv("MODEL_DIR", _cfg.get("model_dir", "./Model"))
CHAT_DIR = Path(os.getenv("CHAT_DIR", _cfg.get("chat_dir", "./Chats")))
CHAT_DIR.mkdir(parents=True, exist_ok=True)

gen_cfg = _cfg.get("generation", {})
model = ModelService(
    MODEL_DIR,
    max_new_tokens=int(gen_cfg.get("max_new_tokens", 64)),
    do_sample=bool(gen_cfg.get("do_sample", False)),
)


def load_model_from_config(config_file='config.json'):
    """
    קוראת את קובץ CONFIG JSON ומחזירה את המודל שטעון ממנו
    """
    config_path = Path(config_file)
    if not config_path.exists():
        raise FileNotFoundError(f"{config_file} לא נמצא")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    model_path = config.get("model_dir")
    if not model_path:
        raise ValueError("לא נמצא 'model_dir' בקובץ CONFIG")

    model_path = Path(model_path)
    if not model_path.exists():
        raise FileNotFoundError(f"המודל לא נמצא בנתיב: {model_path}")

    # טעינת המודל
    model = joblib.load(model_path)
    print(f"מודל נטען מ-{model_path}")
    return model


def model_inference(model, input_data):
    """
    מבצעת אינפרנס למודל ומחזירה את התוצאה
    """
    result = model.predict([input_data])  
    return result[0]

CHAT_FILE = Path("all_chats.json")

def _load_chats():
    if CHAT_FILE.exists():
        return json.loads(CHAT_FILE.read_text(encoding="utf-8"))
    return {"chats": []}

def _save_chat_entry(question: str, answer: str, probability: float, rating=None, links=None):
    data = _load_chats()
    
    id_question = len(data["chats"]) + 1
    
    chat_entry = {
        "id_question": id_question,
        "question": question,
        "answer": answer,
        "rating": rating,          
        "probability": probability, 
        "links": links or {}       
    }
    
    data["chats"].append(chat_entry)
    CHAT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
def mock_quality_score(question: str, answer: str) -> int:

    h = hashlib.blake2b((question + "||" + answer).encode("utf-8"), digest_size=2).digest()
    return int.from_bytes(h, "big") % 101

@app.post("/ask")
def ask(req: Ask):
    ans = model.infer(req.message)
    P = mock_quality_score(req.message, ans) 

   
    _save_chat_entry(
        question=req.message,
        answer=ans,
        probability=P,
        rating=None,
        links={}
    )

    return {"answer": ans, "probability": P}


@app.post("/rate")
def rate(req: RateRequest):

    data = _load_chats()
    
    for chat in data.get("chats", []):
        if chat["id_question"] == req.id_question:
            chat["rating"] = req.rating  
            CHAT_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            return {"status": "ok", "id_question": req.id_question, "rating": req.rating}
    
    return {"status": "error", "message": "id_question not found"}


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", _cfg.get("server", {}).get("host", "0.0.0.0"))
    port = int(os.getenv("PORT", _cfg.get("server", {}).get("port", 8000)))
    uvicorn.run(app, host=host, port=port)