from app.vectorstore.qdrant_client import qdrant_manager

if __name__ == "__main__":
    qdrant_manager.create_collection()