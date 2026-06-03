from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes_upload import router as upload_router
from api.routes_chat import router as chat_router

app = FastAPI(title="AI Chat Backend")

# ----------------------------
# CORS CONFIG (IMPORTANT FIX)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# ROUTES
# ----------------------------
app.include_router(upload_router)
app.include_router(chat_router)
