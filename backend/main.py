from fastapi import FastAPI
from api.routes_chat import router as chat_router
from api.routes_upload import router as upload_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(chat_router)
app.include_router(upload_router)
