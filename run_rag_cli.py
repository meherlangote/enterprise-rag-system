from app.retrieval.hybrid_retriever import hybrid_retriever
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# -----------------------------
# Initialize LLM
# -----------------------------

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0,
)

# -----------------------------
# Prompt Template
# -----------------------------

prompt = ChatPromptTemplate.from_template(
    """
You are an enterprise-grade RAG assistant.

Answer ONLY from the provided context.

If answer is not available in context, say:
"I could not find sufficient information in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
)

# -----------------------------
# CLI LOOP
# -----------------------------

while True:

    query = input("\nEnter your query (or type 'exit'): ")

    if query.lower() == "exit":
        break

    # -----------------------------
    # Retrieve Documents
    # -----------------------------

    results = hybrid_retriever.retrieve(
        query=query,
        k=5,
    )

    if not results:
        print("\nNo relevant documents found.")
        continue

    # -----------------------------
    # Build Context
    # -----------------------------

    context = "\n\n".join(
        [doc.page_content for doc in results]
    )

    # DEBUG
    print("\nRetrieved Context Length:", len(context))

    # -----------------------------
    # Create Prompt
    # -----------------------------

    formatted_prompt = prompt.format(
        context=context,
        question=query,
    )

    # DEBUG
    print("\nGenerating response...\n")

    try:

        response = llm.invoke(formatted_prompt)

        print("=" * 80)
        print("ANSWER:\n")
        print(response.content)
        print("=" * 80)

        # -----------------------------
        # Show Sources
        # -----------------------------

        print("\nSOURCES:\n")

        for idx, doc in enumerate(results):

            print(f"\nSOURCE {idx + 1}")
            print("-" * 50)

            print("METADATA:")
            print(doc.metadata)

    except Exception as e:

        print("\nERROR DURING GENERATION:")
        print(str(e))