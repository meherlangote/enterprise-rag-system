from app.vectorstore.indexing import document_indexer

chunks = [
    {
        "text": "Gradient descent is an optimization algorithm.",
        "page": 1,
        "section": "Optimization",
        "content_type": "text"
    },
    {
        "text": "CNN uses convolution operations for feature extraction.",
        "page": 2,
        "section": "Deep Learning",
        "content_type": "text"
    }
]

document_indexer.index_documents(
    chunks=chunks,
    source_file="ml_book.pdf"
)