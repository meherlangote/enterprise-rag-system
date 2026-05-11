class ContextCompressor:
    def compress(self, documents, max_chars=4000):
        compressed_docs = []

        total_chars = 0

        for doc in documents:
            content_length = len(doc.page_content)

            if total_chars + content_length > max_chars:
                break

            compressed_docs.append(doc)
            total_chars += content_length

        return compressed_docs


context_compressor = ContextCompressor()
