import os

import pytest
from embcli_gemini.gemini import GeminiEmbeddingModel, embedding_model

skip_if_no_api_key = pytest.mark.skipif(
    not os.environ.get("GEMINI_API_KEY") or not os.environ.get("RUN_GEMINI_TESTS") == "1",
    reason="GEMINI_API_KEY and RUN_GEMINI_TESTS environment variables not set",
)


@skip_if_no_api_key
def test_factory_create_valid_model():
    _, create = embedding_model()
    model = create("text-embedding-004")
    assert isinstance(model, GeminiEmbeddingModel)
    assert model.model_id == "text-embedding-004"


@skip_if_no_api_key
def test_factory_create_invalid_model():
    _, create = embedding_model()
    with pytest.raises(ValueError):
        create("invalid-model-id")


@skip_if_no_api_key
def test_embed_one_batch_yields_embeddings(gemini_models):
    for model in gemini_models:
        input_data = ["hello", "world"]
        embeddings = list(model._embed_one_batch(input_data))

        assert len(embeddings) == len(input_data)
        for emb in embeddings:
            assert isinstance(emb, list)
            assert all(isinstance(x, float) for x in emb)


@skip_if_no_api_key
def test_embed_batch_with_options(gemini_models):
    model = gemini_models[0]
    input_data = ["hello", "world"]
    options = {"task_type": "retrieval_document"}

    embeddings = list(model.embed_batch(input_data, None, **options))

    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert isinstance(emb, list)
        assert all(isinstance(x, float) for x in emb)
