import pytest
from embcli_jina import jina, jina_clip
from embcli_jina.jina import JinaEmbeddingModel
from embcli_jina.jina_clip import JinaClipModel


@pytest.fixture
def jina_models():
    model_ids = [alias[0] for alias in JinaEmbeddingModel.model_aliases]
    return [JinaEmbeddingModel(model_id) for model_id in model_ids]


@pytest.fixture
def jina_clip_models():
    model_ids = [alias[0] for alias in JinaClipModel.model_aliases]
    return [JinaClipModel(model_id) for model_id in model_ids]


@pytest.fixture
def plugin_manager():
    """Fixture to provide a pluggy plugin manager."""
    import pluggy
    from embcli_core import hookspecs

    pm = pluggy.PluginManager("embcli")
    pm.add_hookspecs(hookspecs)
    pm.register(jina)
    pm.register(jina_clip)
    return pm
