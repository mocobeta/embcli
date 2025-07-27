from typing import Callable, Optional

import lancedb

from embcli_core.document import Document, DocumentType, HitDocument
from embcli_core.hookspecs import hookimpl
from embcli_core.vector_stores import VectorStoreLocalFS


class LanceDBVectorStore(VectorStoreLocalFS):
    vendor = "lancedb"
    default_persist_path = "./lancedb"

    def __init__(self, persist_path: Optional[str] = None):
        super().__init__(persist_path)
        self.db = lancedb.connect(self.persist_path)

    def _index(self, collection: str, embeddings: list[list[float] | list[int]], docs: list[DocumentType]):
        assert len(embeddings) == len(docs), "Number of embeddings must match number of documents"

        # Prepare data for LanceDB
        data = []
        for doc, embedding in zip(docs, embeddings):
            data.append({"id": doc.docid(), "text": doc.source_text(), "vector": embedding})

        # Create or append to table
        if collection in self.db.table_names():
            table = self.db.open_table(collection)
            table.add(data)
        else:
            # Create table with the first batch of data
            self.db.create_table(collection, data)

    def _search(self, collection: str, query_embedding: list[float] | list[int], top_k: int) -> list[HitDocument]:
        if collection not in self.db.table_names():
            return []

        table = self.db.open_table(collection)
        results = table.search(query_embedding).limit(top_k).to_arrow()

        hits = []

        ids = results.column("id").to_pylist()
        texts = results.column("text").to_pylist()
        distances = results.column("_distance").to_pylist()

        for id_val, text_val, distance in zip(ids, texts, distances):
            # LanceDB returns distance, convert to similarity score
            score = 1.0 / (1.0 + distance)
            doc = Document(id=id_val, text=text_val)
            hits.append(HitDocument(score=score, doc=doc))

        return hits

    def list_collections(self) -> list[str]:
        """List all collections."""
        return list(self.db.table_names())

    def delete_collection(self, collection: str):
        """Delete a collection."""
        if collection in self.db.table_names():
            self.db.drop_table(collection)


@hookimpl
def vector_store() -> tuple[type[LanceDBVectorStore], Callable[[dict], LanceDBVectorStore]]:
    def create(args: dict) -> LanceDBVectorStore:
        return LanceDBVectorStore(**args)

    return LanceDBVectorStore, create
