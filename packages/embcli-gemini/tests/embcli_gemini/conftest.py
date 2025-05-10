import pytest
from embcli_gemini.gemini import GeminiEmbeddingModel


@pytest.fixture
def gemini_models():
    model_ids = [alias[0] for alias in GeminiEmbeddingModel.model_aliases]
    return [GeminiEmbeddingModel(model_id) for model_id in model_ids]
