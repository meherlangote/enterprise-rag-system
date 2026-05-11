from langchain_community.embeddings import HuggingFaceEmbeddings

from app.core.config import settings


class EmbeddingService:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={
                "normalize_embeddings": True
            },
        )

    def embed_documents(self, texts):
        return self.embedding_model.embed_documents(texts)

    def embed_query(self, query):
        return self.embedding_model.embed_query(query)


embedding_service = EmbeddingService()