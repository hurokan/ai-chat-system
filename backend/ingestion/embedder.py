from services.embedding_service import get_embedding
from db.connection import get_conn


class Embedder:

    def __init__(self):
        self.conn = get_conn()
        self.cur = self.conn.cursor()

    def run(self):

        self.cur.execute("""
            SELECT dc.id, dc.content
            FROM document_chunks dc
            LEFT JOIN chunk_embeddings ce
            ON dc.id = ce.chunk_id
            WHERE ce.chunk_id IS NULL
        """)

        rows = self.cur.fetchall()

        print(f"Embedding {len(rows)} chunks")

        for chunk_id, content in rows:

            try:
                embedding = get_embedding(content)

                MODEL_ID = 1  # or whatever exists in embedding_models table

                self.cur.execute("""
                                 INSERT INTO chunk_embeddings (chunk_id,
                                                               embedding,
                                                               model_id)
                                 VALUES (%s, %s, %s)
                                 """, (
                                     chunk_id,
                                     embedding,
                                     MODEL_ID
                                 ))

            except Exception as e:
                print(f"Error chunk {chunk_id}: {e}")

        self.conn.commit()
        print("Embedding completed")