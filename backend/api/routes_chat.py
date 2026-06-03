from fastapi import APIRouter
from models.request_models import ChatRequest
from services.embedding_service import get_embedding
from services.retrieval_service import search_chunks
from services.llm_service import generate_response

router = APIRouter()

@router.post("/chat")
async def chat(req: ChatRequest):

    # 1. Generate embedding
    query_vector = get_embedding(req.message)

    # 2. Retrieve relevant chunks
    chunks = search_chunks(
        document_id=req.document_id,
        vector=query_vector,
        limit=5
    )

    # 3. Safe context handling
    context = "\n".join(chunks) if chunks else "No relevant context found."

    # 4. Prompt construction
    prompt = f"""
You are a helpful assistant.

Use the following context to answer:

Context:
{context}

Question:
{req.message}
"""

    # 5. Generate response
    response = generate_response(prompt)

    return {
        "response": response,
        "chunks_used": len(chunks)
    }
