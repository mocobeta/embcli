import tempfile

import pytest
from embcli_core.document import Document
from embcli_core.vector_store.chroma import ChromaVectorStore


def test_init_with_persist_path():
    # With persist_path using a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        store = ChromaVectorStore(persist_path=tmpdir)
        assert store.client is not None


def test_index_success_and_data_persistence():
    with tempfile.TemporaryDirectory() as tmpdir:
        store = ChromaVectorStore(persist_path=tmpdir)
        embeddings = [[0.1, 0.2], [0.3, 0.4]]
        docs = [Document(id="id1", text="text1"), Document(id="id2", text="text2")]

        collection_name = "test_collection"
        store._index(collection_name, embeddings, docs)

        # Verify data was inserted by querying the collection directly
        collection = store.client.get_or_create_collection(name=collection_name)
        results = collection.query(query_embeddings=[[0.2, 0.3]])
        assert results is not None
        assert results["ids"] is not None
        assert results["documents"] is not None

        # Check that the returned ids match inserted ids
        assert set(results["ids"][0]) == {"id1", "id2"}
        # Check that the documents match
        assert set(results["documents"][0]) == {"text1", "text2"}


def test_index_embedding_doc_length_mismatch():
    with tempfile.TemporaryDirectory() as tmpdir:
        store = ChromaVectorStore(persist_path=tmpdir)
        embeddings = [[0.1, 0.2]]
        docs = [Document(id="id1", text="text1"), Document(id="id2", text="text2")]

        with pytest.raises(AssertionError, match="Number of embeddings must match number of documents"):
            store._index("test_collection", embeddings, docs)
