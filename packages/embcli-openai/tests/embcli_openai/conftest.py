import pytest
from embcli_openai.openai import OpenAIEmbeddingModel


@pytest.fixture
def openai_models():
    model_ids = [alias[0] for alias in OpenAIEmbeddingModel.model_aliases]
    return [OpenAIEmbeddingModel(model_id) for model_id in model_ids]
