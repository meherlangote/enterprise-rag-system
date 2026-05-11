import re

from app.llm.ollama_client import (
    ollama_service,
)


class QueryRewriter:

    def __init__(self):

        self.llm = (
            ollama_service.get_llm()
        )

        self.abbreviations = {
            "cnn": (
                "convolutional neural network"
            ),
            "rnn": (
                "recurrent neural network"
            ),
            "llm": (
                "large language model"
            ),
            "nlp": (
                "natural language processing"
            ),
        }

        self.remove_phrases = [
            "in tabular form",
            "in table",
            "table format",
            "tabular format",
            "show in table",
            "give in table",
        ]

    def clean_query(
        self,
        text: str,
    ):

        text = text.lower()

        # REMOVE NON-ASCII CHARACTERS

        text = re.sub(
            r"[^\x00-\x7F]+",
            " ",
            text,
        )

        # REMOVE FORMATTING PHRASES

        for phrase in self.remove_phrases:

            text = text.replace(
                phrase,
                ""
            )

        # EXPAND ABBREVIATIONS

        for short, full in (
            self.abbreviations.items()
        ):

            text = re.sub(
                rf"\b{short}\b",
                full,
                text,
            )

        # REMOVE EXTRA SPACES

        text = " ".join(
            text.split()
        )

        return text

    def rewrite(
        self,
        query: str,
    ):

        prompt = f"""
Rewrite this query for semantic search retrieval.

Return ONLY the rewritten query.

Query:
{query}
"""

        try:

            response = self.llm.invoke(
                prompt
            )

            rewritten = (
                response.content.strip()
            )

        except Exception:

            rewritten = query

        # POST PROCESSING

        rewritten = self.clean_query(
            rewritten
        )

        return rewritten


query_rewriter = QueryRewriter()