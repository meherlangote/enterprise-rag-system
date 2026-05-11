from langchain_core.prompts import ChatPromptTemplate

from app.llm.ollama_client import ollama_service
from app.prompts.rag_prompt import RAG_PROMPT

from tenacity import (
    retry,
    stop_after_attempt,
    wait_fixed
)

class ResponseGenerator:
    def __init__(self):
        self.llm = ollama_service.get_llm()

        self.prompt = ChatPromptTemplate.from_template(
            RAG_PROMPT
        )

    def build_context(self, documents):
        context_parts = []

        for idx, doc in enumerate(documents, start=1):
            source = doc.metadata.get("source")
            page = doc.metadata.get("page")

            chunk = f"""
                [Source {idx}]
                File: {source}
                Page: {page}

                Content:
                {doc.page_content}
                """

            context_parts.append(chunk)

        return "\n\n".join(context_parts)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(2)
    )
    
    def generate_response(self, question, documents):
        context = self.build_context(documents)

        chain = self.prompt | self.llm

        response = chain.invoke({
            "context": context,
            "question": question
        })

        return response.content


response_generator = ResponseGenerator()