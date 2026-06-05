import uuid
from utils.chunking import chunk_text
from services.embedding_service import get_embedding
from db.connection import get_conn

def ingest_document(filename: str, text: str):

    document_id = str(uuid.uuid4())

    conn = get_conn()
    cur = conn.cursor()

    # insert document
    cur.execute("""
        INSERT INTO documents(document_id, filename)
        VALUES (%s, %s)
    """, (document_id, filename))

    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):

        embedding = get_embedding(chunk)

        cur.execute("""
            INSERT INTO document_chunks
            (document_id, chunk_index, content, embedding)
            VALUES (%s, %s, %s, %s)
        """, (
            document_id,
            i,
            chunk,
            embedding
        ))

    conn.commit()
    cur.close()
    conn.close()

    return document_id
