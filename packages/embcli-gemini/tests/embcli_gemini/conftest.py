import pytest
from embcli_gemini.gemini import GeminiEmbeddingModel


@pytest.fixture
def gemini_model():
    return GeminiEmbeddingModel("text-embedding-004")
