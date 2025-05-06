from typing import Callable, Optional

import embcli_core
from embcli_core.document import DocumentType
from embcli_core.vector_stores import VectorStore, VectorStoreLocalFS


class MockVectorStore(VectorStoreLocalFS):
    vendor = "mock"

    def __init__(self, persist_path: Optional[str] = None):
        super().__init__(persist_path)
        self.cache = {}

    def _index(self, collection: str, embeddings: list[list[float]], docs: list[DocumentType], **kwargs):
        self.cache[collection] = {
            "embeddings": embeddings,
            "documents": [doc.source_text() for doc in docs],
        }


@embcli_core.hookimpl
def vector_store() -> tuple[type[MockVectorStore], Callable[[dict], VectorStore]]:
    def create(args: dict) -> MockVectorStore:
        return MockVectorStore(**args)

    return MockVectorStore, create
