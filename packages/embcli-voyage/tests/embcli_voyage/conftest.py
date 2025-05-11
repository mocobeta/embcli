import pytest
from embcli_voyage.voyage import VoyageEmbeddingModel


@pytest.fixture
def voyage_models():
    model_ids = [alias[0] for alias in VoyageEmbeddingModel.model_aliases]
    return [VoyageEmbeddingModel(model_id) for model_id in model_ids]
