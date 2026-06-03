import requests

OLLAMA_EMBED_URL = "http://ollama:11434/api/embeddings"


def get_embedding(text: str, model: str = "nomic-embed-text"):
    try:
        res = requests.post(
            OLLAMA_EMBED_URL,
            json={
                "model": model,
                "prompt": text
            },
            timeout=30
        )

        res.raise_for_status()
        return res.json()["embedding"]

    except Exception as e:
        print("❌ Embedding error:", e)
        return None
