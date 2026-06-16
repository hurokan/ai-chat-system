from concurrent.futures import ThreadPoolExecutor
from retrieval.vector_search import VectorSearch
from retrieval.keyword_search import KeywordSearch
from retrieval.rrf import RRF


class HybridSearch:

    def __init__(self):

        self.vector = VectorSearch()

        self.keyword = KeywordSearch()

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

            keyword_future = executor.submit(
                self.keyword.search,
                query,
                keyword_limit
            )

            vector_results = (
                vector_future.result()
            )

            keyword_results = (
                keyword_future.result()
            )

        merged = self.rrf.merge(
            vector_results,
            keyword_results
        )

        return merged