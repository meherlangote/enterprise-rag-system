from sentence_transformers import CrossEncoder


class Reranker:
    def __init__(self):

        self.model = CrossEncoder(
            "BAAI/bge-reranker-base"
        )

    def rerank(
        self,
        query,
        documents,
        top_k=3
    ):

        if not documents:
            return []

        pairs = [
            (query, doc.page_content)
            for doc in documents
        ]

        scores = self.model.predict(pairs)

        scored_docs = list(
            zip(documents, scores)
        )

        scored_docs.sort(
            key=lambda x: x[1],
            reverse=True
        )

        reranked_docs = [
            doc
            for doc, score in scored_docs[:top_k]
        ]

        return reranked_docs


reranker = Reranker()