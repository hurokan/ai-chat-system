from db.connection import get_conn

def search_chunks(document_id: str, vector: str, limit: int = 5):
    conn = get_conn()
    cur = conn.cursor()

    if document_id:
        cur.execute("""
            SELECT content
            FROM document_chunks
            WHERE document_id = %s
            ORDER BY embedding <-> %s::vector
            LIMIT %s
        """, (document_id, vector, limit))
    else:
        cur.execute("""
            SELECT content
            FROM document_chunks
            ORDER BY embedding <-> %s::vector
            LIMIT %s
        """, (vector, limit))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [r[0] for r in rows]
