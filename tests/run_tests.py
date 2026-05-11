import time

from app.services.rag_service import (
    rag_service
)

from tests.test_queries import (
    TEST_QUERIES
)

print("\n========================")
print("ENTERPRISE RAG TESTING")
print("========================\n")

success = 0
failure = 0

for idx, test in enumerate(TEST_QUERIES):

    question = test["question"]

    print(f"\nTEST {idx+1}")
    print("-" * 40)

    print(f"QUESTION: {question}")

    start = time.time()

    response = rag_service.ask(question)

    end = time.time()

    latency = round(end - start, 2)

    answer = response["answer"]

    print(f"\nANSWER:\n{answer}")

    print(f"\nLATENCY: {latency} sec")

    # -------------------------
    # REFUSAL CHECK
    # -------------------------

    refusal_text = (
        "I could not find sufficient information"
    )

    if test["expected"] == "refusal":

        if refusal_text in answer:
            print("\nRESULT: PASS")
            success += 1
        else:
            print("\nRESULT: FAIL")
            failure += 1

    else:

        if refusal_text not in answer:
            print("\nRESULT: PASS")
            success += 1
        else:
            print("\nRESULT: FAIL")
            failure += 1

print("\n========================")
print("FINAL RESULTS")
print("========================")

print(f"\nPASSED: {success}")

print(f"FAILED: {failure}")