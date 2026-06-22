from pydantic import BaseModel
from typing import Optional


class ChatSession(BaseModel):
    content: str
    role: Optional[str] = None
    session_id: Optional[str] = None


