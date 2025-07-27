import random
import tempfile

import pytest
from embcli_core.document import Document
from embcli_core.vector_store.lancedb import LanceDBVectorStore


def test_init_with_persist_path():
    # With persist_path using a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        store = LanceDBVectorStore(persist_path=tmpdir)
        assert store.db is not None


def test_index_success_and_data_persistence():
    with tempfile.TemporaryDirectory() as tmpdir:
        store = LanceDBVectorStore(persist_path=tmpdir)
        embeddings = [[0.1, 0.2], [0.3, 0.4]]
        docs = [Document(id="id1", text="text1"), Document(id="id2", text="text2")]

        collection_name = "test_collection"
        store._index(collection_name, embeddings, docs)  # type: ignore

        # Verify data was inserted by checking the table exists and has data
        assert collection_name in store.db.table_names()
        table = store.db.open_table(collection_name)
        arrow_table = table.to_arrow()
        assert arrow_table.num_rows == 2
        ids = arrow_table.column("id").to_pylist()
        texts = arrow_table.column("text").to_pylist()
        assert set(ids) == {"id1", "id2"}
        assert set(texts) == {"text1", "text2"}


def test_index_embedding_doc_length_mismatch():
    with tempfile.TemporaryDirectory() as tmpdir:
        store = LanceDBVectorStore(persist_path=tmpdir)
        embeddings = [[0.1, 0.2]]
        docs = [Document(id="id1", text="text1"), Document(id="id2", text="text2")]

        with pytest.raises(AssertionError, match="Number of embeddings must match number of documents"):
            store._index("test_collection", embeddings, docs)  # type: ignore


def test_search_success():
    with tempfile.TemporaryDirectory() as tmpdir:
        store = LanceDBVectorStore(persist_path=tmpdir)
        embeddings = [[random.uniform(0, 1) for _ in range(10)] for _ in range(10)]
        docs = [Document(id=f"id{i}", text=f"text{i}") for i in range(10)]

        collection_name = "test_collection"
        store._index(collection_name, embeddings, docs)  # type: ignore

        query_embedding = [random.uniform(0, 1) for _ in range(10)]
        top_k = 3
        results = store._search(collection_name, query_embedding, top_k)

        assert len(results) == top_k
        assert all(isinstance(hit.score, float) for hit in results)


def test_search_nonexistent_collection():
    with tempfile.TemporaryDirectory() as tmpdir:
        store = LanceDBVectorStore(persist_path=tmpdir)
        query_embedding = [0.1, 0.2]
        results = store._search("nonexistent_collection", query_embedding, top_k=5)
        assert results == []


def test_list_delete_collections(mock_model):
    with tempfile.TemporaryDirectory() as tmpdir:
        store = LanceDBVectorStore(persist_path=tmpdir)
        collection1 = "collection1"
        collection2 = "collection2"
        docs = [Document(id=f"id{i}", text=f"text{i}") for i in range(10)]

        store.ingest(model=mock_model, collection=collection1, docs=docs)
        store.ingest(model=mock_model, collection=collection2, docs=docs)

        collections = store.list_collections()
        assert len(collections) == 2
        assert collection1 in collections
        assert collection2 in collections

        # Delete one collection
        store.delete_collection(collection1)
        collections = store.list_collections()
        assert len(collections) == 1
        assert collection2 in collections


def test_append_to_existing_collection():
    with tempfile.TemporaryDirectory() as tmpdir:
        store = LanceDBVectorStore(persist_path=tmpdir)
        collection_name = "test_collection"

        # First batch
        embeddings1 = [[0.1, 0.2], [0.3, 0.4]]
        docs1 = [Document(id="id1", text="text1"), Document(id="id2", text="text2")]
        store._index(collection_name, embeddings1, docs1)  # type: ignore

        # Second batch
        embeddings2 = [[0.5, 0.6], [0.7, 0.8]]
        docs2 = [Document(id="id3", text="text3"), Document(id="id4", text="text4")]
        store._index(collection_name, embeddings2, docs2)  # type: ignore

        # Verify all data was appended
        table = store.db.open_table(collection_name)
        arrow_table = table.to_arrow()
        assert arrow_table.num_rows == 4
        ids = arrow_table.column("id").to_pylist()
        assert set(ids) == {"id1", "id2", "id3", "id4"}
