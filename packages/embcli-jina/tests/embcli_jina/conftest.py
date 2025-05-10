import pytest
from embcli_jina.jina import JinaEmbeddingModel


@pytest.fixture
def jina_models():
    model_ids = [alias[0] for alias in JinaEmbeddingModel.model_aliases]
    return [JinaEmbeddingModel(model_id) for model_id in model_ids]
