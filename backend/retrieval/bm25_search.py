from db.connection import get_conn


class BM25Search:

    def search(
        self,
        query,
        limit=30
    ):

        conn = get_conn()
        cur = conn.cursor()

        sql = """
        SELECT
            id,
            document_id,
            filename,
            chunk_index,
            content,
            ts_rank_cd(
                search_vector,
                plainto_tsquery('english', %s)
            ) AS score
        FROM document_chunks
        WHERE search_vector @@ plainto_tsquery('english', %s)
        ORDER BY score DESC
        LIMIT %s
        """

        cur.execute(
            sql,
            (
                query,
                query,
                limit
            )
        )

        rows = cur.fetchall()

        cur.close()
        conn.close()

        results = []

        for rank, row in enumerate(rows, start=1):

            results.append(
                {
                    "chunk_id": row[0],
                    "document_id": str(row[1]),
                    "filename": row[2],
                    "chunk_index": row[3],
                    "content": row[4],
                    "score": float(row[5]),
                    "rank": rank,
                    "source": "bm25"
                }
            )

        return results