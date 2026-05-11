from app.vectorstore.qdrant_client import qdrant_manager


class DenseRetriever:
    def __init__(self):
        self.vectorstore = qdrant_manager.get_vectorstore()

    def retrieve(self, query: str, k: int = 10):
        results = self.vectorstore.similarity_search_with_score(
            query=query,
            k=k,
        )

        documents = []

        for doc, score in results:
            doc.metadata["similarity_score"] = float(score)
            documents.append(doc)

        return documents


dense_retriever = DenseRetriever()