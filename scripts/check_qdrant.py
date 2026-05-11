from app.vectorstore.qdrant_client import (
    qdrant_manager
)

info = qdrant_manager.client.get_collection(
    qdrant_manager.collection_name
)

print("\nCOLLECTION INFO\n")

print(info)