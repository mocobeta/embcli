import pytest
from embcli_sbert.sbert import SBERTEmbeddingModel


@pytest.fixture
def sbert_model():
    return SBERTEmbeddingModel("all-MiniLM-L6-v2")
