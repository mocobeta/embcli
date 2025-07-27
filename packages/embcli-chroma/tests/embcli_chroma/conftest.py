import pytest

from . import mock_embedding_model


@pytest.fixture
def mock_model():
    return mock_embedding_model.MockEmbeddingModel("embedding-mock-1")
