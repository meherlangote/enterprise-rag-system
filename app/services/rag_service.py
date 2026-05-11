from app.retrieval.pipeline import retrieval_pipeline
from app.llm.generator import response_generator

from app.cache.semantic_cache import semantic_cache
from app.core.logger import logger
from app.guardrails.hallucination_detector import (
    hallucination_detector
)

from app.guardrails.response_validator import (
    response_validator
)

class RAGService:

    def ask(self, question: str):

        logger.info(
            f"Received question: {question}"
        )

        # -------------------------
        # CACHE CHECK
        # -------------------------

        cached_response = semantic_cache.get(question)

        if cached_response:

            logger.info(
                "Response served from cache"
            )

            cached_response["cache_hit"] = True

            return cached_response

        # -------------------------
        # RETRIEVAL
        # -------------------------

        logger.info(
            "Starting retrieval..."
        )

        retrieval_results = retrieval_pipeline.retrieve(
            question
        )

        documents = retrieval_results["documents"]

        logger.info(
            f"Retrieved {len(documents)} documents"
        )

        # -------------------------
        # HALLUCINATION CHECK
        # -------------------------

        retrieval_valid = (
            hallucination_detector.validate_retrieval(
                documents
            )
        )

        if not retrieval_valid:

            logger.warning(
                "Rejected response due to low confidence"
            )

            response = {
                "answer": (
                    response_validator.refusal_response()
                ),
                "citations": [],
                "cache_hit": False
            }

            semantic_cache.set(question, response)

            return response

        # -------------------------
        # GENERATION
        # -------------------------

        logger.info(
            "Generating response..."
        )

        answer = response_generator.generate_response(
            question=question,
            documents=documents
        )

        # -------------------------
        # RESPONSE VALIDATION
        # -------------------------

        answer_valid = (
            response_validator.validate_answer(
                answer
            )
        )

        if not answer_valid:

            logger.warning(
                "Rejected response due to invalid answer"
            )

            response = {
                "answer": (
                    response_validator.refusal_response()
                ),
                "citations": [],
                "cache_hit": False
            }

            semantic_cache.set(question, response)

            return response

        # -------------------------
        # FINAL RESPONSE
        # -------------------------

        logger.info(
            "Response generated successfully"
        )

        response = {
            "answer": answer,
            "citations": retrieval_results["citations"],
            "cache_hit": False
        }

        semantic_cache.set(question, response)

        return response


rag_service = RAGService()