from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat_routes
from app.config import HOST_SERVER, PORT_SERVER
from app.routes import message_routes

app = FastAPI(title="Main Server Chatbot")

# ✅ הוספת CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # או צייני מקור ספציפי כמו "http://localhost:5173"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# רישום הראוטים
app.include_router(chat_routes.router, prefix="/api/message")
app.include_router(message_routes.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST_SERVER, port=PORT_SERVER)
