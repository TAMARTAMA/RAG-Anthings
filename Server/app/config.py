from pathlib import Path
import json

CFG_PATH = Path(__file__).with_name("..") / "config.json"
cfg = json.loads(Path(CFG_PATH).read_text(encoding="utf-8"))

PORT_SERVER = cfg["server"]["port"]
HOST_SERVER = cfg["server"]["host"]
SERVER_MODEL_URL = cfg["remote_server"]["url_LLM"]

BASE_DIR = Path(__file__).resolve().parents[1]
CHATS_FILE = (BASE_DIR / Path(cfg["chats_name"]))
RATINGS_FILE = (BASE_DIR / Path(cfg["ratings_name"]))



