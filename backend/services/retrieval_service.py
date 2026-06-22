from config.settings import FINAL_TOP_K
from retrieval.hybrid_search import HybridSearch
from services.embedding_service import get_embedding


class RetrievalService:

    def __init__(self):
        self.hybrid = HybridSearch()

    def retrieve(
        self,
        query,
        top_k=FINAL_TOP_K
    ):

        query_embedding = get_embedding(query)

        results = self.hybrid.search(
            query,
            query_embedding
        )

        print("=" * 60)
        print("TOP HYBRID RESULTS")
        print("=" * 60)

        for item in results[:10]:

            print(
                f"Chunk={item.get('chunk_id')} | "
                f"Source={item.get('source')} | "
                f"RRF={item.get('rrf_score', 0)}"
            )

        return results[:top_k]

    def build_context(
        self,
        query,
        top_k=FINAL_TOP_K
    ):

        chunks = self.retrieve(
            query,
            top_k
        )

        context_parts = []
        total_length = 0

        max_length = 1500

        for chunk in chunks:

            content = chunk.get(
                "content",
                ""
            )

            content = content[:500]

            if (
                total_length +
                len(content)
                > max_length
            ):
                break

            context_parts.append(
                content
            )

            total_length += len(
                content
            )

        return "\n\n".join(
            context_parts
        )