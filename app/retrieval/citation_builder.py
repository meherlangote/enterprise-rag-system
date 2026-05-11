class CitationBuilder:
    def build_citations(self, documents):
        citations = []

        for idx, doc in enumerate(documents, start=1):
            citation = {
                "id": idx,
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page"),
                "section": doc.metadata.get("section"),
                "similarity_score": doc.metadata.get(
                    "similarity_score"
                ),
                "rerank_score": doc.metadata.get(
                    "rerank_score"
                ),
            }

            citations.append(citation)

        return citations


citation_builder = CitationBuilder()