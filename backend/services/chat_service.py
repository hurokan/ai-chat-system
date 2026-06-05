import requests
from services.retrieval_service import retrieve_context

OLLAMA_CHAT_URL = "http://ollama:11434/api/generate"

def generate_answer(message: str):

    chunks = retrieve_context(message)

    context = "\n\n".join([c[0] for c in chunks])

    prompt = f"""
Use context to answer:

Context:
{context}

Question:
{message}
"""

    res = requests.post(
        OLLAMA_CHAT_URL,
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    return {
        "response": res.json().get("response", ""),
        "sources": chunks
    }
