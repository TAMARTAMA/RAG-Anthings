# Main Server Chatbot (FastAPI)

שרת FastAPI קטן שמשמש כ־Gateway לבקשות NLP: הוא מקבל שאלה מהלקוחה, שולח אותה לשרת מודל חיצוני יחד עם System Prompt, ומחזיר את התשובה (או קיד־וורדס) ללקוחה. בנוסף יש נקודת קצה לדרוג תשובה.

## ✨ פיצ’רים
- `POST /ask` – מקבל שאלה (`message`) ומחזיר תשובה/מילות מפתח ע״פ מודל מרוחק.
- `POST /rate` – מקבל דירוג לתשובה קיימת (`id_question`, `rating`) ושומר דרך שכבת `chat_history`.
- קונפיגורציה דרך `config.json` (פורט/הוסט, URL של שרת המודל).
- טיפול בסיסי בשגיאות תקשורת עם השרת המרוחק.

---

## 📁 מבנה הפרויקט (מוצע)
```
.
├─ main.py                 # הקובץ עם הקוד שצירפת
├─ config.json             # קובץ קונפיגורציה (ראה דוגמה מטה)
├─ models.py               # הגדרות Pydantic ל-Ask/RateRequest
├─ chat_history.py         # add_chat / update_rate / get_all_chats
├─ prompts_model.py        # system_prompt_keywords, system_prompt_guess, ...
├─ requirements.txt        # תלויות פייתון
└─ README.md
```

---

## ⚙️ קונפיגורציה (`config.json`)
דוגמה לקובץ מינימלי:
```json
{

  "chat_dir": "all_chats",
  "server": {
    "host": "0.0.0.0",
    "port": 8002
  },
  "remote_server": {
    "url": "http://127.0.0.1:8014/generate"
  }
}
```
- `server.host` / `server.port` – עליהם ירוץ שרת ה־FastAPI.
- `remote_server.url` – כתובת ה־HTTP שאליה נשלח ה־payload של המודל (ראה `send_data_to_server`).

> שים/י לב: `main.py` קורא את הקובץ הזה יחסית למיקום הקובץ עצמו (`CFG_PATH = Path(__file__).with_name("config.json")`), אז הקובץ צריך לשבת ליד `main.py`.

---

## 🧾 מודלים (Pydantic) – דוגמה קונקרטית
```python
# models.py
from pydantic import BaseModel
from typing import Optional, Literal

class Ask(BaseModel):
    session: Optional[str] = None
    message: str

class RateRequest(BaseModel):
    id_question: str
    rating: Literal["like", "dislike", "neutral"] | int
```

---

## 📦 התקנה והפעלה

1) צור/י סביבה והתקן/י חבילות:
```bash
python -m venv .venv
source .venv/bin/activate   # ב-Windows: .venv\Scriptsctivate
pip install -r requirements.txt
```


2) ודא/י שקיים `config.json` תקין (כמו בדוגמה למעלה).

3) הרצה:
```bash
python main.py
# או דרך uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

4) עמודי שירות:
- Swagger: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

> אם מריצים עם `uvicorn main:app`, הפרמטרים בשורת הפקודה גוברים על ה־config.

---

## 🔌 נקודות קצה (API)

### `POST /ask`
Body:
```json
{
  "message": "מה זה BM25 ואיך הוא שונה מ-TF-IDF?",
  "session": "optional-session-id"
}
```
Response (דוגמאות):
```json
{ "answer": ["bm25", "idf", "tf", "okapi bm25", "retrieval"] }
```
או טקסט:
```json
{ "answer": "bm25, idf, tf, okapi bm25, retrieval" }
```

**curl:**
```bash
curl -X POST http://localhost:8000/ask   -H "Content-Type: application/json"   -d '{"message":"תני 10 קידוורדס לתשובה על BM25"}'
```

### `POST /rate`
Body:
```json
{
  "id_question": "6f0cfdc2a3e94d89bff22d4c1b9e8f05",
  "rating": "like"
}
```
Response:
```json
{ "status": "ok" }
```

**curl:**
```bash
curl -X POST http://localhost:8000/rate   -H "Content-Type: application/json"   -d '{"id_question":"<ID-EXISTS>", "rating":"dislike"}'
```

---

## 🧠 לוגיקה מרכזית
- `process_asking(question)` עוטפת את הקריאה ל־`send_data_to_server` עם `system_prompt_keywords`.
- `send_data_to_server(url, question, system_prompt)` שולחת payload בסגנון Chat API עם `requests.post` ומחזירה JSON/טקסט.

---

## 🗃️ chat_history (אופציונלי)
השלימו את `add_chat`, `update_rate`, `get_all_chats` לפי הצורך.
אפשר להחזיר מ־`/ask` גם `id_question` לשימוש ב־`/rate`.

---

## 🛡️ CORS
אם צריך גישה מ־Web Origin אחר:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🧪 בדיקות
```bash
curl -s http://localhost:8000/docs > /dev/null && echo "API up!"
```

---

## 🔒 אבטחה
- לצמצם CORS בייצור.
- לא לשמור סודות ב־Git. שקלו .env.
- ולאמת קלטים היטב.

---

## 📜 רישיון
בחרו רישיון (MIT/Apache-2.0/וכו׳) והוסיפו קובץ `LICENSE`.

---

### טיפ: בחירת פרומפט דינמית
```python
@app.post("/ask")
def ask(req: Ask, prompt: str = "keywords"):
    prompt_map = {
        "keywords": system_prompt_keywords,
        "guess": system_prompt_guess,
        "more_question": system_prompt_more_question,
        "bm25_q": system_prompt_bm25_q,
    }
    system_prompt = prompt_map.get(prompt, system_prompt_keywords)
    ans = send_data_to_server(SERVER_MODEL_URL, req.message, system_prompt)
    return {"answer": ans, "prompt_used": prompt}
```
