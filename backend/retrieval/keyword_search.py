from db.connection import get_conn


class KeywordSearch:

    def search(self, query, limit=30):

        conn = get_conn()

        try:
            with conn.cursor() as cur:

                sql = """
                WITH q AS (
                    SELECT plainto_tsquery('english', %s) AS query
                )
                SELECT
                    id,
                    document_id,
                    chunk_index,
                    content,
                    metadata,
                    ts_rank_cd(search_vector, q.query) AS score
                FROM document_chunks, q
                WHERE search_vector @@ q.query
                ORDER BY score DESC
                LIMIT %s;
                """

                cur.execute(sql, (query, limit))
                rows = cur.fetchall()

                return [
                    {
                        "chunk_id": row[0],
                        "document_id": str(row[1]),
                        "chunk_index": row[2],
                        "content": row[3],
                        "metadata": row[4],
                        "score": float(row[5]),
                        "rank": i,
                        "source": "keyword"
                    }
                    for i, row in enumerate(rows, 1)
                ]

        finally:
            conn.close()