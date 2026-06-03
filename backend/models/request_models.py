from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    document_id: Optional[str] = None
    session_id: Optional[str] = None
