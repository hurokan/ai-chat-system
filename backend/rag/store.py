from sqlalchemy import create_engine, text

engine = create_engine(
    "postgresql://admin:admin123@postgres:5432/ai_chat"
)

def store_chunk(content, embedding):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO documents (content, embedding)
            VALUES (:content, :embedding)
        """), {
            "content": content,
            "embedding": embedding
        })
