import random
from typing import Callable, Optional

import embcli_core
from embcli_core.document import DocumentType, HitDocument
from embcli_core.vector_stores import VectorStore, VectorStoreLocalFS


class MockVectorStore(VectorStoreLocalFS):
    vendor = "mock"
    default_persist_path = "./mockdb"

    def __init__(self, persist_path: Optional[str] = None):
        super().__init__(persist_path)
        self.cache = {}

    def _index(self, collection: str, embeddings: list[list[float]], docs: list[DocumentType]):
        self.cache[collection] = {
            "embeddings": embeddings,
            "documents": docs,
        }

    def _search(self, collection: str, query_embedding: list[float], top_k: int) -> list[HitDocument]:
        if collection not in self.cache:
            return []
        docs = random.sample(self.cache[collection]["documents"], top_k)
        hits = [HitDocument(score=random.uniform(0, 1), doc=doc) for doc in docs]
        return hits

    def list_collections(self) -> list[str]:
        """List all collections."""
        return list(self.cache.keys())

    def delete_collection(self, collection: str):
        """Delete a collection."""
        if collection in self.cache:
            del self.cache[collection]


@embcli_core.hookimpl
def vector_store() -> tuple[type[MockVectorStore], Callable[[dict], VectorStore]]:
    def create(args: dict) -> MockVectorStore:
        return MockVectorStore(**args)

    return MockVectorStore, create
