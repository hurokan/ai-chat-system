import requests

from config.settings import (
    OLLAMA_BASE_URL,
    OLLAMA_EMBED_MODEL
)

OLLAMA_EMBED_URL = (
    f"{OLLAMA_BASE_URL}/api/embeddings"
)


def get_embedding(text: str):

    response = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": OLLAMA_EMBED_MODEL,
            "prompt": text
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    if "embedding" not in data:
        raise Exception(
            f"Invalid Ollama response: {data}"
        )

    return data["embedding"]