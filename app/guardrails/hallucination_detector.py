class HallucinationDetector:
    def __init__(
        self,
        min_similarity=0.60,
        min_rerank=0.20,
        min_docs=1,
    ):
        self.min_similarity = min_similarity
        self.min_rerank = min_rerank
        self.min_docs = min_docs

    def validate_retrieval(self, documents):
        if len(documents) < self.min_docs:
            return False

        valid_docs = 0

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
                similarity >= self.min_similarity
                and rerank >= self.min_rerank
            ):
                valid_docs += 1

        return valid_docs >= self.min_docs


hallucination_detector = HallucinationDetector()