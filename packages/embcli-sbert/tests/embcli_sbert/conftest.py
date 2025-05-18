import pytest
from embcli_sbert import sbert
from embcli_sbert.sbert import SentenceTransformerModel


@pytest.fixture
def sbert_model():
    return SentenceTransformerModel("sentence-transformers", local_model_id="all-MiniLM-L6-v2")


@pytest.fixture
def plugin_manager():
    """Fixture to provide a pluggy plugin manager."""
    import pluggy
    from embcli_core import hookspecs

    pm = pluggy.PluginManager("embcli")
    pm.add_hookspecs(hookspecs)
    pm.register(sbert)
    return pm
