from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)


class SemanticChunker:

    def __init__(
        self,
        chunk_size=800,
        chunk_overlap=150
    ):

        self.text_splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=[
                    "\n\n",
                    "\n",
                    ". ",
                    " ",
                    ""
                ]
            )
        )

    def chunk_documents(
        self,
        documents
    ):

        chunks = (
            self.text_splitter.split_documents(
                documents
            )
        )

        return chunks