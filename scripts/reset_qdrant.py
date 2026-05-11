from app.vectorstore.qdrant_client import qdrant_manager

qdrant_manager.client.delete_collection(
    collection_name=qdrant_manager.collection_name
)

print("Old collection deleted")

qdrant_manager.create_collection()

print("Fresh collection created")