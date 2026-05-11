from pathlib import Path

from app.ingestion.pdf_loader import PDFLoader

from ingestion.chunking.semantic_chunker import (
    SemanticChunker,
)

from app.vectorstore.qdrant_client import (
    qdrant_manager,
)

RAW_DATA_PATH = Path("data/raw")

pdf_loader = PDFLoader()

chunker = SemanticChunker()


def process_pdf(pdf_path):

    print(f"\nProcessing: {pdf_path.name}")

    # -------------------------
    # LOAD PDF
    # -------------------------

    documents = pdf_loader.load_pdf(
        str(pdf_path)
    )

    print(f"Loaded {len(documents)} pages")

    # -------------------------
    # CHUNKING
    # -------------------------

    chunks = chunker.chunk_documents(
        documents
    )

    print(f"Generated {len(chunks)} chunks")

    # -------------------------
    # ADD METADATA
    # -------------------------

    for i, chunk in enumerate(chunks):

        chunk.metadata["source"] = (
            pdf_path.name
        )

        chunk.metadata["chunk_id"] = i

    # -------------------------
    # INSERT INTO QDRANT
    # -------------------------

    qdrant_manager.add_documents(
        chunks
    )

    print(
        f"Inserted {len(chunks)} chunks into Qdrant"
    )


def main():

    pdf_files = list(
        RAW_DATA_PATH.glob("*.pdf")
    )

    print(f"\nFound {len(pdf_files)} PDFs")

    for pdf_path in pdf_files:

        try:

            process_pdf(pdf_path)

        except Exception as e:

            print(
                f"\nFailed processing "
                f"{pdf_path.name}"
            )

            print(str(e))


if __name__ == "__main__":

    main()