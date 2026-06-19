from fastapi import APIRouter
from pydantic import BaseModel

from services.chat_service import (
    generate_answer
)

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    session_id: str


@router.post("/chat")
def chat(req: ChatRequest):

    answer = generate_answer(
        req.message,
        req.session_id
    )

    return {
        "response": answer
    }