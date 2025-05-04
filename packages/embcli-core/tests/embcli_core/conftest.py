import pytest

from . import mock_embedding_model


@pytest.fixture
def mock_model():
    return mock_embedding_model.MockEmbeddingModel("embedding-mock-1")


@pytest.fixture
def plugin_manager():
    """Fixture to provide a pluggy plugin manager."""
    import pluggy
    from embcli_core import hookspecs

    pm = pluggy.PluginManager("embcli")
    pm.add_hookspecs(hookspecs)
    pm.register(mock_embedding_model)

    return pm
