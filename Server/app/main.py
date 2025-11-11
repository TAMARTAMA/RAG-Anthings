from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat_routes
from app.routes import prob_route
from app.config import HOST_SERVER, PORT_SERVER
from app.routes import auth_routes  

app = FastAPI(title="Main Server Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_routes.router, prefix="/api/message")
app.include_router(auth_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST_SERVER, port=PORT_SERVER)
