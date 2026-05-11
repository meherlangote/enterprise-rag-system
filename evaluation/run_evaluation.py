import pandas as pd

from datasets import Dataset

from ragas import evaluate

from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

from langchain_ollama import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings

from app.services.rag_service import rag_service
from app.retrieval.pipeline import retrieval_pipeline

from evaluation.sample_dataset import (
    evaluation_data
)

# -----------------------------------
# LOCAL OLLAMA LLM
# -----------------------------------

evaluator_llm = LangchainLLMWrapper(
    ChatOllama(
        model="qwen2.5:3b",
        temperature=0
    )
)

# -----------------------------------
# LOCAL EMBEDDINGS
# -----------------------------------

evaluator_embeddings = LangchainEmbeddingsWrapper(
    HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )
)

# -----------------------------------
# DATA COLLECTION
# -----------------------------------

questions = []
answers = []
contexts = []
ground_truths = []

# -----------------------------------
# GENERATE RAG RESPONSES
# -----------------------------------

from pathlib import Path

cache_file = Path("data/cache/cache.json")

if cache_file.exists():
    cache_file.unlink()

for item in evaluation_data:

    question = item["question"]

    rag_response = rag_service.ask(question)

    retrieval_response = (
        retrieval_pipeline.retrieve(question)
    )

    context_list = [
        doc.page_content
        for doc in retrieval_response["documents"]
    ]

    questions.append(question)

    answers.append(rag_response["answer"])

    contexts.append(context_list)

    ground_truths.append(item["ground_truth"])

# -----------------------------------
# CREATE DATASET
# -----------------------------------

dataset = Dataset.from_dict({
    "question": questions,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": ground_truths,
})

# -----------------------------------
# RUN RAGAS EVALUATION
# -----------------------------------

result = evaluate(
    dataset=dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    ],
    llm=evaluator_llm,
    embeddings=evaluator_embeddings,
)

# -----------------------------------
# RESULTS
# -----------------------------------

df = result.to_pandas()

print("\n==============================")
print("RAGAS EVALUATION RESULTS")
print("==============================\n")

print(df)

print("\n==============================")
print("AVERAGE SCORES")
print("==============================\n")

print(df.mean(numeric_only=True))