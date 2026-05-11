from app.retrieval.retriever import dense_retriever
from app.retrieval.reranker import reranker
from app.retrieval.confidence import confidence_filter
from app.retrieval.compression import context_compressor
from app.retrieval.citation_builder import citation_builder


class RetrievalPipeline:
    def remove_duplicates(self, documents):
        unique_docs = []
        seen = set()

        for doc in documents:
            chunk_id = doc.metadata.get("chunk_id")

            if chunk_id not in seen:
                seen.add(chunk_id)
                unique_docs.append(doc)

        return unique_docs

    def retrieve(self, query: str):
        dense_results = dense_retriever.retrieve(
            query=query,
            k=6
        )

        reranked_docs = reranker.rerank(
            query=query,
            documents=dense_results,
            top_k=3
        )

        unique_docs = self.remove_duplicates(
            reranked_docs
        )

        filtered_docs = confidence_filter.filter_documents(
            unique_docs
        )

        compressed_docs = context_compressor.compress(
            filtered_docs
        )

        citations = citation_builder.build_citations(
            compressed_docs
        )

        return {
            "documents": compressed_docs,
            "citations": citations
        }


retrieval_pipeline = RetrievalPipeline()