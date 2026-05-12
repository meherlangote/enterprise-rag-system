from app.vectorstore.qdrant_client import (
    qdrant_manager,
)

from sentence_transformers import (
    CrossEncoder,
)

import ollama


# ===================================
# QUERY REWRITER
# ===================================

class QueryRewriter:

    def rewrite(self, query):

        try:

            prompt = f"""
You are a query rewriting assistant
for a Retrieval-Augmented Generation system.

Rewrite the query ONLY to improve retrieval.

STRICT RULES:
- Preserve all technical keywords
- Preserve abbreviations like CNN, RNN, LSTM
- Do NOT remove important words
- Do NOT answer the question
- Keep rewrite close to original query
- Add clarity only if necessary

Return ONLY the rewritten query.

User Query:
{query}
"""

            response = ollama.chat(

                model="qwen2.5:3b",

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            rewritten_query = (
                response["message"]["content"]
                .strip()
            )

            print(
                f"\nRewritten Query: "
                f"{rewritten_query}"
            )

            return rewritten_query

        except Exception as e:

            print(
                f"\nQuery rewriting failed: {e}"
            )

            return query


# ===================================
# CROSS-ENCODER RERANKER
# ===================================

class Reranker:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(self, query, docs):

        try:

            if not docs:
                return []

            # CREATE QUERY-DOCUMENT PAIRS

            pairs = [

                (
                    query,
                    doc.page_content
                )

                for doc in docs
            ]

            # PREDICT RELEVANCE SCORES

            scores = self.model.predict(
                pairs
            )

            # COMBINE DOCS + SCORES

            scored_docs = list(
                zip(docs, scores)
            )

            # SORT DESCENDING

            scored_docs.sort(

                key=lambda x: x[1],

                reverse=True
            )

            # EXTRACT ONLY DOCS

            reranked_docs = [

                doc

                for doc, score
                in scored_docs
            ]

            print(
                f"\nReranked documents: "
                f"{len(reranked_docs)}"
            )

            return reranked_docs[:5]

        except Exception as e:

            print(
                f"\nReranking failed: {e}"
            )

            return docs


# ===================================
# HYBRID RETRIEVER
# ===================================

class HybridRetriever:

    def __init__(self):

        self.vectorstore = (
            qdrant_manager.get_vectorstore()
        )

        self.query_rewriter = (
            QueryRewriter()
        )

        self.reranker = (
            Reranker()
        )

    def retrieve(self, query, k=20):

        try:

            # -------------------------
            # QUERY REWRITING
            # -------------------------

            rewritten_query = (

                self.query_rewriter.rewrite(
                    query
                )
            )

            # -------------------------
            # VECTOR SEARCH
            # -------------------------

            docs = (

                self.vectorstore.max_marginal_relevance_search(
                    rewritten_query,
                    k=k,
                    fetch_k=50
                )
            )

            print(
                f"\nRetrieved from vector DB:"
                f" {len(docs)}"
            )

            # -------------------------
            # RERANKING
            # -------------------------

            reranked_docs = (

                self.reranker.rerank(

                    rewritten_query,

                    docs
                )
            )

            # -------------------------
            # DEBUG OUTPUT
            # -------------------------

            if reranked_docs:

                print(
                    "\nFIRST RERANKED CHUNK:\n"
                )

                print(

                    reranked_docs[0]
                    .page_content[:700]
                )

            return reranked_docs

        except Exception as e:

            print(
                f"\nRetrieval failed: {e}"
            )

            return []


# ===================================
# SINGLETON INSTANCE
# ===================================

hybrid_retriever = HybridRetriever()