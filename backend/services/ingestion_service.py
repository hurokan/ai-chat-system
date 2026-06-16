import uuid
import hashlib
from utils.chunking import chunk_text
from services.embedding_service import get_embeddings_batch
from db.connection import get_conn


def generate_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def ingest_document(filename: str, text: str):

    document_id = str(uuid.uuid4())
    file_hash = generate_hash(text)

    conn = get_conn()
    cur = conn.cursor()

    try:
        # -----------------------------
        # 1. INSERT DOCUMENT META ONLY
        # -----------------------------
        cur.execute("""
            INSERT INTO documents (document_id, filename, file_hash, status)
            VALUES (%s, %s, %s, %s)
        """, (document_id, filename, file_hash, "processing"))

        # -----------------------------
        # 2. CHUNK TEXT
        # -----------------------------
        chunks = chunk_text(text)
        print("Chunks:", len(chunks))


        if not chunks:
            raise Exception("No chunks generated")

        # -----------------------------
        # 3. BATCH EMBEDDINGS
        # -----------------------------
        embeddings = get_embeddings_batch(chunks)
        print("Embedding sample:", len(embeddings[0]))
        # -----------------------------
        # 4. STORE CHUNKS
        # -----------------------------
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            print(type(embedding))
            print(embedding[:5])
            try:
                cur.execute("""
                            INSERT INTO document_chunks
                                (document_id, chunk_index, content, embedding, content_hash)
                            VALUES (%s, %s, %s, %s, %s)
                            """, (
                                document_id,
                                i,
                                chunk,
                                embedding,
                                hashlib.sha256(chunk.encode()).hexdigest()
                            ))
            except Exception as e:
                print("FAILED CHUNK:", i)
                print(e)
                raise

        # -----------------------------
        # 5. MARK COMPLETE
        # -----------------------------
        cur.execute("""
            UPDATE documents
            SET status = %s
            WHERE document_id = %s
        """, ("ready", document_id))

        conn.commit()

        return document_id

    except Exception as e:
        conn.rollback()

        cur.execute("""
            UPDATE documents
            SET status = %s
            WHERE document_id = %s
        """, ("failed", document_id))

        conn.commit()

        raise e

    finally:
        cur.close()
        conn.close()