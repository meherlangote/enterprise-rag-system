from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # =====================================================
    # APPLICATION
    # =====================================================

    APP_NAME: str
    APP_ENV: str
    DEBUG: bool

    # =====================================================
    # API
    # =====================================================

    API_HOST: str
    API_PORT: int

    # =====================================================
    # OLLAMA
    # =====================================================

    OLLAMA_BASE_URL: str
    OLLAMA_MODEL: str
    OLLAMA_TEMPERATURE: float = 0.0
    OLLAMA_TIMEOUT: int = 120

    # =====================================================
    # QDRANT
    # =====================================================

    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION: str

    # IMPORTANT
    QDRANT_VECTOR_DIMENSION: int

    QDRANT_DISTANCE_METRIC: str = "Cosine"

    # =====================================================
    # EMBEDDINGS
    # =====================================================

    EMBEDDING_MODEL: str
    EMBEDDING_DEVICE: str = "cpu"

    EMBEDDING_BATCH_SIZE: int = 16

    # =====================================================
    # RERANKER
    # =====================================================

    ENABLE_RERANKING: bool = True

    RERANKER_MODEL: str
    RERANK_TOP_K: int = 5

    # =====================================================
    # CHUNKING
    # =====================================================

    CHUNK_SIZE: int
    CHUNK_OVERLAP: int

    SEMANTIC_SIMILARITY_THRESHOLD: float = 0.65

    # =====================================================
    # RETRIEVAL
    # =====================================================

    TOP_K: int
    FINAL_TOP_K: int = 5

    SIMILARITY_THRESHOLD: float

    # =====================================================
    # CACHE
    # =====================================================

    ENABLE_SEMANTIC_CACHE: bool = True

    # =====================================================
    # PATHS
    # =====================================================

    RAW_DATA_PATH: str
    PROCESSED_DATA_PATH: str
    CACHE_PATH: str

    # =====================================================
    # Pydantic Config
    # =====================================================

    model_config = {

        "env_file": ".env",

        "extra": "ignore",
    }


# =========================================================
# SETTINGS INSTANCE
# =========================================================

settings = Settings()










# from pydantic_settings import BaseSettings, SettingsConfigDict
# from pydantic import field_validator

# class Settings(BaseSettings):
#     QDRANT_HOST: str = "localhost"
#     QDRANT_PORT: int = 6333
#     QDRANT_COLLECTION: str = "technical_documents"

#     EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

#     RERANKER_MODEL: str = "BAAI/bge-reranker-base"
    
#     OLLAMA_BASE_URL: str = "http://localhost:11434"
#     OLLAMA_MODEL: str = "qwen2.5:3b"
    
#     model_config = SettingsConfigDict(
#         env_file=".env",
#         extra="ignore"
#     )
    
#     similarity_threshold: float = 0.70
    
#     @field_validator("similarity_threshold")
    
#     def validate_threshold(cls, v):
#         if v < 0 or v > 1:
#             raise ValueError(
#                 "similarity_threshold must be between 0 and 1"
#             )

#         return v


# settings = Settings()