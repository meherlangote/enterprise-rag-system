import hashlib
import json
from pathlib import Path

from app.embeddings.embedding_service import (
    embedding_service
)


class SemanticCache:
    def __init__(self):
        self.cache_path = Path("data/cache/cache.json")

        self.cache_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.cache_path.exists():
            self.cache_path.write_text("{}")

    def load_cache(self):

        if not self.cache_path.exists():
            self.cache_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            self.cache_path.write_text("{}")

        with open(self.cache_path, "r") as f:
            return json.load(f)

    def save_cache(self, cache_data):
        with open(self.cache_path, "w") as f:
            json.dump(cache_data, f, indent=2)

    def generate_key(self, query):
        return hashlib.sha256(
            query.encode()
        ).hexdigest()

    def get(self, query):
        cache = self.load_cache()

        key = self.generate_key(query)

        return cache.get(key)

    def set(self, query, response):
        cache = self.load_cache()

        key = self.generate_key(query)

        cache[key] = response

        self.save_cache(cache)


semantic_cache = SemanticCache()