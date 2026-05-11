class RAGException(Exception):
    pass


class RetrievalException(RAGException):
    pass


class EmbeddingException(RAGException):
    pass


class LLMException(RAGException):
    pass