from db.connection import get_conn


class VectorSearch:

    def search(
        self,
        query_embedding,
        limit=30
    ):

        conn = get_conn()

        try:

            with conn.cursor() as cur:

                vector_str = (
                    "[" +
                    ",".join(
                        str(v)
                        for v in query_embedding
                    ) +
                    "]"
                )

                sql = """
                SELECT
                    dc.id,
                    dc.document_id,
                    dc.chunk_index,
                    dc.content,
                    dc.metadata,
                    dc.embedding <=> %s::vector AS distance

                FROM document_chunks dc

                WHERE dc.embedding IS NOT NULL

                ORDER BY dc.embedding <=> %s::vector

                LIMIT %s
                """

                cur.execute(
                    sql,
                    (
                        vector_str,
                        vector_str,
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
                            "distance": float(row[5]),
                            "rank": rank,
                            "source": "vector"
                        }
                    )

                    rank += 1

                return results

        finally:
            conn.close()