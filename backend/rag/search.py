from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql://admin:admin123@postgres:5432/ai_chat"
)

def search_similar(embedding, limit=5):
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT content
            FROM documents
            ORDER BY embedding <-> :embedding
            LIMIT :limit
        """), {
            "embedding": embedding,
            "limit": limit
        })

        return [row[0] for row in result]
