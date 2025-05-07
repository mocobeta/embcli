from importlib import resources

import pytest

from . import mock_embedding_model, mock_vector_store


@pytest.fixture
def mock_model():
    return mock_embedding_model.MockEmbeddingModel("embedding-mock-1")


@pytest.fixture
def mock_store():
    return mock_vector_store.MockVectorStore("persist_path")


@pytest.fixture
def plugin_manager():
    """Fixture to provide a pluggy plugin manager."""
    import pluggy
    from embcli_core import hookspecs

    pm = pluggy.PluginManager("embcli")
    pm.add_hookspecs(hookspecs)
    pm.register(mock_embedding_model)
    pm.register(mock_vector_store)
    return pm


@pytest.fixture
def test_csv_file() -> str:
    file_path = resources.path("embcli_core.synth_data", "fake_cat_names.csv")
    return str(file_path)
