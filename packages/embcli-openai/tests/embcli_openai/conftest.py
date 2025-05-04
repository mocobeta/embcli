import pytest
from embcli_openai.openai import OpenAIEmbeddingModel


@pytest.fixture
def openai_model():
    return OpenAIEmbeddingModel("text-embedding-3-small")
