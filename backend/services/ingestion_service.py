import re
from services.embedding_service import get_embedding
from db.connection import get_conn
from utils.chunking import chunk_text


def clean_text(text: str) -> str:
    if not text:
        return ""

    # remove NULL bytes (CRITICAL FIX)
    text = text.replace("\x00", "")

    # remove control chars
    text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", text)

    # normalize spaces
    text = " ".join(text.split())

    return text


def ingest_document(document_id, filename, text):

    conn = get_conn()
    cur = conn.cursor()

    chunks = chunk_text(text)

    inserted = 0

    for i, chunk in enumerate(chunks):

        chunk = clean_text(chunk)

        if not chunk.strip():
            continue

        try:
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

            inserted += 1

        except Exception as e:
            print(f"❌ CHUNK {i} FAILED:", e)
            continue

    conn.commit()
    cur.close()
    conn.close()

    print("✅ INSERTED:", inserted)
