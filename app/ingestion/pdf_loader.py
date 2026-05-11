import fitz

from langchain_core.documents import Document

class PDFLoader:

    def load_pdf(self, pdf_path):

        documents = []

        pdf = fitz.open(pdf_path)

        for page_num in range(len(pdf)):

            page = pdf[page_num]

            text = page.get_text()

            if text.strip():

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": pdf_path,
                            "page": page_num + 1
                        }
                    )
                )

        return documents