import os

import pytest
from embcli_openai.openai import OpenAIEmbeddingModel, embedding_model

skip_if_no_api_key = pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY") or not os.environ.get("RUN_OPENAI_TESTS") == "1",
    reason="OPENAI_API_KEY and RUN_OPENAI_TESTS environment variables not set",
)


@skip_if_no_api_key
def test_factory_create_valid_model():
    _, create = embedding_model()
    model = create("text-embedding-3-small")
    assert isinstance(model, OpenAIEmbeddingModel)
    assert model.model_id == "text-embedding-3-small"


@skip_if_no_api_key
def test_factory_create_invalid_model():
    _, create = embedding_model()
    with pytest.raises(ValueError):
        create("invalid-model-id")


@skip_if_no_api_key
def test_embed_one_batch_yields_embeddings(openai_models):
    for model in openai_models:
        input_data = ["hello", "world"]

        embeddings = list(model._embed_one_batch(input_data))

        assert len(embeddings) == len(input_data)
        for emb in embeddings:
            assert isinstance(emb, list)
            assert all(isinstance(x, float) for x in emb)


@skip_if_no_api_key
def test_embed_batch_with_options(openai_models):
    model = openai_models[0]
    input_data = ["hello", "world"]
    options = {"dimensions": "128"}

    embeddings = list(model.embed_batch(input_data, None, **options))

    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert len(emb) == 128
