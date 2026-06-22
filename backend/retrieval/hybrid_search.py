from concurrent.futures import ThreadPoolExecutor

from retrieval.vector_search import (
    VectorSearch
)

from retrieval.bm25_search import (
    BM25Search
)

from retrieval.rrf import (
    RRF
)


class HybridSearch:

    def __init__(self):

        self.vector = VectorSearch()

        self.bm25 = BM25Search()

        self.rrf = RRF()

    def search(
        self,
        query,
        query_embedding,
        vector_limit=30,
        keyword_limit=30
    ):

        with ThreadPoolExecutor(
            max_workers=2
        ) as executor:

            vector_future = executor.submit(
                self.vector.search,
                query_embedding,
                vector_limit
            )

            bm25_future = executor.submit(
                self.bm25.search,
                query,
                keyword_limit
            )

            vector_results = (
                vector_future.result()
            )

            bm25_results = (
                bm25_future.result()
            )

        merged = self.rrf.merge(
            vector_results,
            bm25_results
        )

        return merged