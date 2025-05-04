import os

import pytest


@pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY") or not os.environ.get("RUN_OPENAI_TESTS") == "1",
    reason="OPENAI_API_KEY and RUN_OPENAI_TESTS environment variables not set",
)
def test_initialization_sets_model_id_and_client(openai_model):
    model = openai_model
    assert model.model_id == "text-embedding-3-small"
    assert model.client is not None


@pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY") or not os.environ.get("RUN_OPENAI_TESTS") == "1",
    reason="OPENAI_API_KEY and RUN_OPENAI_TESTS environment variables not set",
)
def test_embed_one_batch_calls_openai_and_yields_embeddings(openai_model):
    model = openai_model
    input_data = ["hello", "world"]

    embeddings = list(model._embed_one_batch(input_data))

    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert isinstance(emb, list)
        assert all(isinstance(x, float) for x in emb)


@pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY") or not os.environ.get("RUN_OPENAI_TESTS") == "1",
    reason="OPENAI_APIKEY and RUN_OPENAI_TESTS environment variables not set",
)
def test_embed_batch_with_options(openai_model):
    model = openai_model
    input_data = ["hello", "world"]
    options = {"dimensions": "128"}

    embeddings = list(model.embed_batch(input_data, None, **options))

    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert len(emb) == 128
