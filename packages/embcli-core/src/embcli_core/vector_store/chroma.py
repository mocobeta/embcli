from typing import Callable, Optional

import chromadb

from embcli_core.document import DocumentType
from embcli_core.hookspecs import hookimpl
from embcli_core.vector_stores import VectorStoreLocalFS


class ChromaVectorStore(VectorStoreLocalFS):
    vendor = "chroma"
    default_persist_path = "./chroma"

    def __init__(self, persist_path: Optional[str] = None):
        super().__init__(persist_path)
        self.client = chromadb.PersistentClient(path=self.persist_path)

    def _index(self, collection: str, embeddings: list[list[float]], docs: list[DocumentType]):
        assert len(embeddings) == len(docs), "Number of embeddings must match number of documents"
        # Create or get the collection
        chroma_collection = self.client.get_or_create_collection(name=collection)
        chroma_collection.upsert(
            ids=[doc.docid() for doc in docs],
            embeddings=embeddings,  # type: ignore
            documents=[doc.source_text() for doc in docs],
        )


@hookimpl
def vector_store() -> tuple[type[ChromaVectorStore], Callable[[dict], ChromaVectorStore]]:
    def create(args: dict) -> ChromaVectorStore:
        return ChromaVectorStore(**args)

    return ChromaVectorStore, create
