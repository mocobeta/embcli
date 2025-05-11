import pytest
from embcli_mistral.mistral import MistralEmbeddingModel


@pytest.fixture
def mistral_models():
    model_ids = [alias[0] for alias in MistralEmbeddingModel.model_aliases]
    return [MistralEmbeddingModel(model_id) for model_id in model_ids]
