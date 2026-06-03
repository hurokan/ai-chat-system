from db.connection import get_conn
from services.embedding_service import get_embedding
from utils.vector import to_vector_string


def retrieve_context(query: str, document_id: str, top_k: int = 5):

    conn = get_conn()
    cur = conn.cursor()

    query_embedding = get_embedding(query)

    cur.execute(
        """
        SELECT content
        FROM documents
        WHERE document_id = %s
        ORDER BY embedding <-> %s::vector
        LIMIT %s
        """,
        (document_id, to_vector_string(query_embedding), top_k)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return "\n".join([r[0] for r in rows])
