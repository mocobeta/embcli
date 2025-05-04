from embcli_core.models import avaliable_models, get_model
from embcli_core.plugins import register_models

from . import mock_embedding_model


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
