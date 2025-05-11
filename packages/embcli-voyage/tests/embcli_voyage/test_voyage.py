import os

import pytest
from embcli_voyage.voyage import VoyageEmbeddingModel, embedding_model

skip_if_no_api_key = pytest.mark.skipif(
    not os.environ.get("VOYAGE_API_KEY") or not os.environ.get("RUN_VOYAGE_TESTS") == "1",
    reason="VOYAGE_API_KEY and RUN_VOYAGE_TESTS environment variables not set",
)


@skip_if_no_api_key
def test_factory_create_valid_model():
    _, create = embedding_model()
    model = create("voyage-3")
    assert isinstance(model, VoyageEmbeddingModel)
    assert model.model_id == "voyage-3"


@skip_if_no_api_key
def test_factory_create_invalid_model():
    _, create = embedding_model()
    with pytest.raises(ValueError):
        create("invalid-model-id")


@skip_if_no_api_key
def test_embed_one_batch_yields_embeddings(voyage_models):
    for model in voyage_models:
        input_data = ["hello", "world"]

        embeddings = list(model._embed_one_batch(input_data))

        assert len(embeddings) == len(input_data)
        for emb in embeddings:
            assert isinstance(emb, list)
            assert all(isinstance(x, float) for x in emb)


@skip_if_no_api_key
def test_embed_batch_with_options(voyage_models):
    model = voyage_models[0]
    input_data = ["hello", "world"]
    options = {"input_type": "query", "truncation": False, "output_dimension": "512"}

    embeddings = list(model.embed_batch(input_data, None, **options))

    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert len(emb) == 512
