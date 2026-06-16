from db.connection import get_conn
from ingestion.chunker import chunk_text


class Loader:

    def __init__(self):
        self.conn = get_conn()
        self.cur = self.conn.cursor()

    def run(self):

        self.cur.execute("""
            SELECT id, content
            FROM documents
            WHERE content IS NOT NULL
        """)

        docs = self.cur.fetchall()

        for doc_id, content in docs:

            chunks = chunk_text(content)

            for idx, chunk in enumerate(chunks):

                self.cur.execute("""
                    INSERT INTO document_chunks (
                        document_id,
                        content,
                        chunk_index
                    )
                    VALUES (%s, %s, %s)
                """, (doc_id, chunk, idx))

        self.conn.commit()
        print("Chunking completed")