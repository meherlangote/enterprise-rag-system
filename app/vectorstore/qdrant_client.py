from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
)

from langchain_qdrant import (
    QdrantVectorStore,
)

from app.core.config import settings

from app.embeddings.embedding_service import (
    embedding_service,
)


class QdrantManager:

    def __init__(self):

        # =====================================================
        # CONNECT TO QDRANT
        # =====================================================

        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )

        self.collection_name = (
            settings.QDRANT_COLLECTION
        )

        # =====================================================
        # ENSURE COLLECTION EXISTS
        # =====================================================

        self._create_collection_if_not_exists()

        # =====================================================
        # INITIALIZE VECTOR STORE
        # =====================================================

        self.vectorstore = QdrantVectorStore(
            client=self.client,

            collection_name=self.collection_name,

            embedding=embedding_service.embedding_model,
        )

        print(
            f"\nQdrant VectorStore Ready: "
            f"{self.collection_name}"
        )

    # =========================================================
    # CREATE COLLECTION IF MISSING
    # =========================================================

    def _create_collection_if_not_exists(
        self
    ):

        try:

            collections = (
                self.client.get_collections()
            )

            existing_collections = [

                collection.name

                for collection
                in collections.collections
            ]

            # =================================================
            # CREATE COLLECTION ONLY IF NOT EXISTS
            # =================================================

            if (
                self.collection_name
                not in existing_collections
            ):

                print(
                    f"\nCreating collection: "
                    f"{self.collection_name}"
                )

                self.client.create_collection(

                    collection_name=(
                        self.collection_name
                    ),

                    vectors_config=VectorParams(

                        size=(
                            settings
                            .QDRANT_VECTOR_DIMENSION
                        ),

                        distance=Distance.COSINE,
                    ),
                )

                print(
                    "\nCollection created successfully."
                )

            else:

                print(
                    f"\nCollection already exists: "
                    f"{self.collection_name}"
                )

        except Exception as e:

            raise RuntimeError(

                f"\nFailed to initialize "
                f"Qdrant collection.\n"
                f"Error: {str(e)}"
            )

    # =========================================================
    # ADD DOCUMENTS
    # =========================================================

    def add_documents(
        self,
        documents,
        ids=None,
    ):

        try:

            self.vectorstore.add_documents(
                documents=documents,
                ids=ids,
            )

            print(
                f"\nIndexed "
                f"{len(documents)} documents"
            )

        except Exception as e:

            raise RuntimeError(

                f"\nDocument indexing failed.\n"
                f"Error: {str(e)}"
            )

    # =========================================================
    # SIMILARITY SEARCH
    # =========================================================

    def similarity_search(
        self,
        query,
        k=5,
    ):

        try:

            results = (
                self.vectorstore
                .similarity_search(

                    query=query,
                    k=k,
                )
            )

            return results

        except Exception as e:

            raise RuntimeError(

                f"\nSimilarity search failed.\n"
                f"Error: {str(e)}"
            )

    # =========================================================
    # SIMILARITY SEARCH WITH SCORE
    # =========================================================

    def similarity_search_with_score(
        self,
        query,
        k=5,
    ):

        try:

            results = (
                self.vectorstore
                .similarity_search_with_score(

                    query=query,
                    k=k,
                )
            )

            return results

        except Exception as e:

            raise RuntimeError(

                f"\nSimilarity search "
                f"with score failed.\n"
                f"Error: {str(e)}"
            )

    # =========================================================
    # GET VECTORSTORE
    # =========================================================

    def get_vectorstore(self):

        return self.vectorstore

    # =========================================================
    # DELETE COLLECTION
    # =========================================================

    def delete_collection(self):

        try:

            self.client.delete_collection(
                collection_name=self.collection_name
            )

            print(
                f"\nDeleted collection: "
                f"{self.collection_name}"
            )

        except Exception as e:

            raise RuntimeError(

                f"\nFailed to delete "
                f"collection.\n"
                f"Error: {str(e)}"
            )


# =============================================================
# SINGLETON INSTANCE
# =============================================================

qdrant_manager = QdrantManager()