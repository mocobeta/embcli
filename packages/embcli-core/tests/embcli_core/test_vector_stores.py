from embcli_core.document import Document
from embcli_core.vector_stores import available_vector_stores, get_vector_store, register


def test_ingest(mock_model, mock_store, mocker):
    spy1 = mocker.spy(mock_store, "_index")
    spy2 = mocker.spy(mock_model, "embed_batch")
    collection = "test_collection"
    documents = [Document("doc1", "This is a test document."), Document("doc2", "Another test document.")]
    mock_store.ingest(mock_model, collection, documents)
    assert spy1.call_count == 1
    assert spy2.call_count == 1


def test_ingest_with_batch_size(mock_model, mock_store, mocker):
    spy1 = mocker.spy(mock_store, "_index")
    spy2 = mocker.spy(mock_model, "embed_batch")
    collection = "test_collection"
    documents = [Document(f"doc{i}", "This is a test document.") for i in range(10)]
    batch_size = 3
    mock_store.ingest(mock_model, collection, documents, batch_size=batch_size)
    assert spy1.call_count == 4  # Three batches of 3, 3, and 4 documents
    assert spy2.call_count == 4


def test_register(mocker):
    mock_vector_store_cls = mocker.Mock()  # Mocking the vector store class
    mock_vector_store_cls.vendor = "mock"
    mock_vector_store_instance = mocker.Mock()  # Mocking the vector store instance
    mock_factory = mocker.Mock(return_value=mock_vector_store_instance)  # Mocking the factory function

    register(mock_vector_store_cls, mock_factory)

    assert mock_vector_store_cls in available_vector_stores()
    assert get_vector_store("mock", {"persist_path": "./mydb"}) == mock_vector_store_instance
