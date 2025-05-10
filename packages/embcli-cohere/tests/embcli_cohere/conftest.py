import pytest
from embcli_cohere.cohere_model import CohereEmbeddingModel


@pytest.fixture
def cohere_models():
    model_ids = [alias[0] for alias in CohereEmbeddingModel.model_aliases]
    return [CohereEmbeddingModel(model_id) for model_id in model_ids]
