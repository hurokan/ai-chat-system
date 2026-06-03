from pypdf import PdfReader
import os

from db.connection import get_conn
from services.embedding_service import get_embedding
from utils.vector import to_vector_string


# =========================
# TEXT EXTRACTION
# =========================
def extract_text(file_path: str):
    reader = PdfReader(file_path)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text

    return text


# =========================
# CHUNKING
# =========================
def chunk_text(text: str, size: int = 500):
    return [text[i:i + size] for i in range(0, len(text), size)]


# =========================
# MAIN INGESTION FUNCTION (FIXED)
# =========================
def store_document(file_path: str, filename: str):

    text = extract_text(file_path)
    chunks = chunk_text(text)

    conn = get_conn()
    cur = conn.cursor()

    inserted = 0
    failed = 0

    print("🔥 INGESTION STARTED")
    print("TOTAL CHUNKS:", len(chunks))

    for i, chunk in enumerate(chunks):

        try:
            embedding = get_embedding(chunk)

            # safety check
            if not embedding:
                raise Exception("Empty embedding returned")

            cur.execute(
                """
                INSERT INTO documents
                (document_id, filename, chunk_index, content, embedding)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    filename,
                    filename,
                    i,
                    chunk,
                    to_vector_string(embedding)
                )
            )

            inserted += 1

        except Exception as e:
            # IMPORTANT FIX → rollback per failure
            conn.rollback()
            print(f"❌ CHUNK {i} FAILED:", e)
            failed += 1

        else:
            # commit only successful insert
            conn.commit()

    cur.close()
    conn.close()

    print("✅ INGESTION DONE")
    print("INSERTED:", inserted)
    print("FAILED:", failed)

    return {
        "chunks": len(chunks),
        "inserted": inserted,
        "failed": failed
    }