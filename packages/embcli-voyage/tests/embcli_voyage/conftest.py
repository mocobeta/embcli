import pytest
from embcli_voyage import voyage, voyage_multimodal
from embcli_voyage.voyage import VoyageEmbeddingModel
from embcli_voyage.voyage_multimodal import VoyageMultimodalEmbeddingModel


@pytest.fixture
def voyage_models():
    model_ids = [alias[0] for alias in VoyageEmbeddingModel.model_aliases]
    return [VoyageEmbeddingModel(model_id) for model_id in model_ids]


@pytest.fixture
def voyage_multimodal_models():
    model_ids = [alias[0] for alias in VoyageMultimodalEmbeddingModel.model_aliases]
    return [VoyageMultimodalEmbeddingModel(model_id) for model_id in model_ids]


@pytest.fixture
def plugin_manager():
    """Fixture to provide a pluggy plugin manager."""
    import pluggy
    from embcli_core import hookspecs

    pm = pluggy.PluginManager("embcli")
    pm.add_hookspecs(hookspecs)
    pm.register(voyage)
    pm.register(voyage_multimodal)
    return pm
