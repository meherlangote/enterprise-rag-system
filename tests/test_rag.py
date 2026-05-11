from app.services.rag_service import rag_service

query = "What is gradient descent?"

response = rag_service.ask(query)

print("\nANSWER:\n")
print(response["answer"])

print("\nCITATIONS:\n")

for citation in response["citations"]:
    print(citation)