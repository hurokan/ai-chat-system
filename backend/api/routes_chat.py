from fastapi import APIRouter
from pydantic import BaseModel
from services.chat_service import generate_answer

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@router.post("/chat")
def chat(req: ChatRequest):
    return {
        "answer": generate_answer(req.message)
    }