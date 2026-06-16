from db.connection import get_conn


class KeywordSearch:

    def search(
        self,
        query,
        limit=30
    ):

        conn = get_conn()

        try:

            with conn.cursor() as cur:

                sql = """
                SELECT
                    id,
                    document_id,
                    chunk_index,
                    content,
                    metadata,

                    ts_rank(
                        search_vector,
                        plainto_tsquery('english', %s)
                    ) AS score

                FROM document_chunks

                WHERE search_vector @@
                    plainto_tsquery(
                        'english',
                        %s
                    )

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

                results = []

                rank = 1

                for row in rows:

                    results.append(
                        {
                            "chunk_id": row[0],
                            "document_id": str(row[1]),
                            "chunk_index": row[2],
                            "content": row[3],
                            "metadata": row[4],
                            "score": float(row[5]),
                            "rank": rank,
                            "source": "keyword"
                        }
                    )

                    rank += 1

                return results

        finally:
            conn.close()