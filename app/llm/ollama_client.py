from langchain_ollama import ChatOllama

from app.core.config import settings


class OllamaService:
    def __init__(self):
        self.llm = ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.1,
            num_predict=512,
            request_timeout=120
        )

    def get_llm(self):
        return self.llm


ollama_service = OllamaService()