import pytest
from embcli_jina import jina, jina_multimodal
from embcli_jina.jina import JinaEmbeddingModel
from embcli_jina.jina_multimodal import JinaMultiModalModel


@pytest.fixture
def jina_models():
    model_ids = [alias[0] for alias in JinaEmbeddingModel.model_aliases]
    return [JinaEmbeddingModel(model_id) for model_id in model_ids]


@pytest.fixture
def jina_multimodal_models():
    model_ids = [alias[0] for alias in JinaMultiModalModel.model_aliases]
    return [JinaMultiModalModel(model_id) for model_id in model_ids]


@pytest.fixture
def plugin_manager():
    """Fixture to provide a pluggy plugin manager."""
    import pluggy
    from embcli_core import hookspecs

    pm = pluggy.PluginManager("embcli")
    pm.add_hookspecs(hookspecs)
    pm.register(jina)
    pm.register(jina_multimodal)
    return pm
