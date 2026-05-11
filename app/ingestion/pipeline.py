import fitz
import re

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)


class IngestionPipeline:
    def __init__(self):

        self.splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=600,
                chunk_overlap=120,
                separators=[
                    "\n# ",
                    "\n## ",
                    "\n\n",
                    "\n",
                    ". ",
                    " ",
                    ""
                ]
            )
        )

    def clean_text(self, text):
        text = re.sub(r'\s+', ' ', text)

        text = text.strip()

        return text

    def extract_text(self, pdf_path):
        doc = fitz.open(pdf_path)

        pages = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            text = page.get_text()

            text = self.clean_text(text)

            pages.append({
                "page": page_num + 1,
                "text": text
            })

        return pages

    def process_pdf(self, pdf_path):
        pages = self.extract_text(pdf_path)

        chunks = []

        for page_data in pages:

            split_texts = self.splitter.split_text(
                page_data["text"]
            )

            for chunk_text in split_texts:

                if len(chunk_text.strip()) < 80:
                    continue

                chunk = {
                    "text": chunk_text,
                    "page": page_data["page"],
                    "section": "Unknown",
                    "content_type": "text"
                }

                chunks.append(chunk)

        return chunks


ingestion_pipeline = IngestionPipeline()