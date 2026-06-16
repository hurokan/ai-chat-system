from collections import defaultdict


class RRF:

    def __init__(self, k=60):
        self.k = k

    def score(self, rank):

        return 1.0 / (
            self.k + rank
        )

    def merge(
        self,
        vector_results,
        keyword_results
    ):

        scores = defaultdict(float)

        chunk_map = {}

        for item in vector_results:

            chunk_id = item["chunk_id"]

            scores[chunk_id] += self.score(
                item["rank"]
            )

            chunk_map[chunk_id] = item

        for item in keyword_results:

            chunk_id = item["chunk_id"]

            scores[chunk_id] += self.score(
                item["rank"]
            )

            chunk_map[chunk_id] = item

        final = []

        for chunk_id, score in scores.items():

            row = chunk_map[chunk_id]

            row["rrf_score"] = score

            final.append(row)

        final.sort(
            key=lambda x: x["rrf_score"],
            reverse=True
        )

        return final