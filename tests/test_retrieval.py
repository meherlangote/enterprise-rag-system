from app.retrieval.hybrid_retriever import (
    hybrid_retriever,
)

query = input(
    "\nEnter your query: "
)

results = hybrid_retriever.retrieve(
    query=query,
    k=5,
)

print("\nRETRIEVED DOCUMENTS\n")

for idx, doc in enumerate(results):

    print(f"\nRESULT {idx + 1}")
    print("-" * 50)

    print("CONTENT:\n")
    print(doc.page_content)

    print("\nMETADATA:")
    print(doc.metadata)