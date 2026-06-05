from db.connection import get_conn
from services.embedding_service import get_embedding

def retrieve_context(query: str, limit: int = 5):

    conn = get_conn()
    cur = conn.cursor()

    q_embedding = get_embedding(query)

    cur.execute("""
        SELECT content, document_id
        FROM document_chunks
        ORDER BY embedding <-> %s::vector
        LIMIT %s
    """, (str(q_embedding), limit))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows
