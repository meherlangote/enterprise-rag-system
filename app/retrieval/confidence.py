class ConfidenceFilter:
    def __init__(
        self,
        similarity_threshold=0.75,
        rerank_threshold=0.35,
    ):
        self.similarity_threshold = similarity_threshold
        self.rerank_threshold = rerank_threshold

    def filter_documents(self, documents):
        filtered = []

        for doc in documents:
            similarity = doc.metadata.get(
                "similarity_score",
                0
            )

            rerank = doc.metadata.get(
                "rerank_score",
                0
            )

            if (
                similarity >= self.similarity_threshold
                and rerank >= self.rerank_threshold
            ):
                filtered.append(doc)

        return filtered


confidence_filter = ConfidenceFilter()