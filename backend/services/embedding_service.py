# FILE: services/embedding_service.py

import requests
from typing import List

from config.settings import (
    OLLAMA_BASE_URL,
    OLLAMA_EMBED_MODEL
)

OLLAMA_EMBED_URL = f"{OLLAMA_BASE_URL}/api/embeddings"


# =========================================================
# SINGLE EMBEDDING (USED IN RETRIEVAL)
# =========================================================
def get_embedding(text: str) -> List[float]:

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

    embedding = data.get("embedding")

    if not embedding:
        raise Exception(f"Empty embedding response: {data}")

    return embedding


# =========================================================
# BATCH EMBEDDING (USED IN INGESTION)
# =========================================================
def get_embeddings_batch(texts: List[str]) -> List[List[float]]:

    embeddings = []

    for text in texts:
        embeddings.append(get_embedding(text))

    return embeddings