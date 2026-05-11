import hashlib
from uuid import uuid4

from langchain_core.documents import Document

from app.vectorstore.qdrant_client import qdrant_manager


class DocumentIndexer:
    def __init__(self):
        self.vectorstore = qdrant_manager.get_vectorstore()

    def generate_chunk_id(self, text: str):
        return hashlib.sha256(text.encode()).hexdigest()

    def prepare_documents(self, chunks, source_file):
        documents = []

        for chunk in chunks:
            chunk_id = self.generate_chunk_id(chunk["text"])

            metadata = {
                "chunk_id": chunk_id,
                "source": source_file,
                "page": chunk.get("page", 0),
                "section": chunk.get("section", "unknown"),
                "content_type": chunk.get("content_type", "text"),
            }

            doc = Document(
                page_content=chunk["text"],
                metadata=metadata,
            )

            documents.append(doc)

        return documents

    def index_documents(self, chunks, source_file):
        documents = self.prepare_documents(chunks, source_file)

        ids = [str(uuid4()) for _ in documents]

        self.vectorstore.add_documents(
            documents=documents,
            ids=ids,
        )

        print(f"Indexed {len(documents)} chunks")


document_indexer = DocumentIndexer()