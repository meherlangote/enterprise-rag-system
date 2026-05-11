from app.vectorstore.qdrant_client import (
    qdrant_manager,
)


class HybridRetriever:

    def __init__(self):
        self.vectorstore = qdrant_manager.get_vectorstore()

    def retrieve(self, query, k=10):

        # -------------------------
        # VECTOR SEARCH (DIRECT QUERY)
        # -------------------------

        docs = self.vectorstore.similarity_search(
            query,
            k=k
        )

        print(f"\nRetrieved from vector DB: {len(docs)}")

        # PRINT FIRST CHUNK (debug)
        if docs:
            print("\nFIRST RETRIEVED CHUNK:\n")
            print(docs[0].page_content[:500])

        return docs


hybrid_retriever = HybridRetriever()