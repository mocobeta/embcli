import os

import pytest
from embcli_cohere.cohere_model import CohereEmbeddingModel, embedding_model

skip_if_no_api_key = pytest.mark.skipif(
    not os.environ.get("COHERE_API_KEY") or not os.environ.get("RUN_COHERE_TESTS") == "1",
    reason="COHERE_API_KEY and RUN_COHERE_TESTS environment variables not set",
)


@skip_if_no_api_key
def test_factory_create_valid_model():
    _, create = embedding_model()
    model = create("embed-v4.0")
    assert isinstance(model, CohereEmbeddingModel)
    assert model.model_id == "embed-v4.0"


@skip_if_no_api_key
def test_factory_create_invalid_model():
    _, create = embedding_model()
    with pytest.raises(ValueError):
        create("invalid-model-id")


@skip_if_no_api_key
def test_embed_one_batch_yields_embeddings(cohere_models):
    for model in cohere_models:
        input_data = ["hello", "world"]

        embeddings = list(model._embed_one_batch(input_data))

        assert len(embeddings) == len(input_data)
        for emb in embeddings:
            assert isinstance(emb, list)
            assert all(isinstance(x, float) for x in emb)


@skip_if_no_api_key
def test_embed_batch_with_options(cohere_models):
    model = cohere_models[0]
    input_data = ["hello", "world"]
    options = {"input_type": "classification", "truncate": "end"}

    embeddings = list(model.embed_batch(input_data, None, **options))

    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert isinstance(emb, list)
        assert all(isinstance(x, float) for x in emb)


@skip_if_no_api_key
def test_embed_batch_for_ingest(cohere_models, mocker):
    for model in cohere_models:
        input_data = ["hello", "world"]
        spy = mocker.spy(model, "embed_batch")
        embeddings = list(model.embed_batch_for_ingest(input_data, None))
        assert len(embeddings) > 0

        # Check that the spy was called with the correct model options
        spy.assert_called_once_with(input_data, None, input_type="search_document")


@skip_if_no_api_key
def test_embed_for_search(cohere_models, mocker):
    for model in cohere_models:
        input = "hello world"
        spy = mocker.spy(model, "embed")
        embedding = list(model.embed_for_search(input))
        assert len(embedding) > 0

        # Check that the spy was called with the correct model options
        spy.assert_called_once_with(input, input_type="search_query")
