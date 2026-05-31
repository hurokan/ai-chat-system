import requests

OLLAMA_URL = "http://ollama:11434/api/embeddings"

def get_embedding(text: str):
    res = requests.post(
        OLLAMA_URL,
        json={
            "model": "nomic-embed-text",
            "prompt": text
        }
    )

    return res.json()["embedding"]
