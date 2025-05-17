from typing import Callable, Optional

import chromadb

from embcli_core.document import Document, DocumentType, HitDocument
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

    def _search(self, collection: str, query_embedding: list[float], top_k: int) -> list[HitDocument]:
        chroma_collection = self.client.get_or_create_collection(name=collection)
        results = chroma_collection.query(
            query_embeddings=[query_embedding], n_results=top_k, include=["documents", "distances"]
        )
        if not results["documents"] or not results["ids"] or not results["distances"]:
            return []
        hits = []
        for doc_text, doc_id, distance in zip(results["documents"][0], results["ids"][0], results["distances"][0]):
            score = 1.0 / (1.0 + distance)
            doc = Document(id=doc_id, text=doc_text)
            hits.append(HitDocument(score=score, doc=doc))
        return hits

    def list_collections(self) -> list[str]:
        """List all collections."""
        collections = self.client.list_collections()
        return [collection.name for collection in collections]

    def delete_collection(self, collection: str):
        """Delete a collection."""
        self.client.delete_collection(name=collection)


@hookimpl
def vector_store() -> tuple[type[ChromaVectorStore], Callable[[dict], ChromaVectorStore]]:
    def create(args: dict) -> ChromaVectorStore:
        return ChromaVectorStore(**args)

    return ChromaVectorStore, create
