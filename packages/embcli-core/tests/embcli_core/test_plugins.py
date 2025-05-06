from embcli_core.document import Document
from embcli_core.models import avaliable_models, get_model
from embcli_core.plugins import register_models, register_vector_stores
from embcli_core.vector_stores import available_vector_stores, get_vector_store

from . import mock_embedding_model, mock_vector_store


def test_register_models(plugin_manager):
    register_models(plugin_manager)

    # Check if the models are registered correctly
    assert mock_embedding_model.MockEmbeddingModel in avaliable_models()

    # Check if the factory function is registered correctly
    model = get_model("embedding-mock-1")
    assert model is not None
    assert all(isinstance(x, float) for x in model.embed("test input"))

    model = get_model("mock1")
    assert model is not None
    assert all(isinstance(x, float) for x in model.embed("test input"))


def test_register_vector_stores(plugin_manager):
    register_vector_stores(plugin_manager)

    # Check if the vector stores are registered correctly
    assert mock_vector_store.MockVectorStore in available_vector_stores()

    # Check if the factory function is registered correctly
    vector_store = get_vector_store("mock", {"persist_path": "./mydb"})
    assert vector_store is not None
    assert isinstance(vector_store, mock_vector_store.MockVectorStore)
    model = get_model("embedding-mock-1")
    assert model is not None

    # Check if the instanciated vector store works correctly
    vector_store.ingest(
        model,
        "test_collection",
        [Document("doc1", "This is a test document."), Document("doc2", "Another test document.")],
    )
    data = vector_store.cache["test_collection"]
    assert data["documents"] == [
        Document("doc1", "This is a test document."),
        Document("doc2", "Another test document."),
    ]
    assert len(data["embeddings"]) == 2
