import os

import pytest
from embcli_mistral.mistral import MistralEmbeddingModel, embedding_model

skip_if_no_api_key = pytest.mark.skipif(
    not os.environ.get("MISTRAL_API_KEY") or not os.environ.get("RUN_MISTRAL_TESTS") == "1",
    reason="MISTRAL_API_KEY and RUN_MISTRAL_TESTS environment variables not set",
)


@skip_if_no_api_key
def test_factory_create_valid_model():
    _, create = embedding_model()
    model = create("mistral-embed")
    assert isinstance(model, MistralEmbeddingModel)
    assert model.model_id == "mistral-embed"


@skip_if_no_api_key
def test_factory_create_invalid_model():
    _, create = embedding_model()
    with pytest.raises(ValueError):
        create("invalid-model-id")


@skip_if_no_api_key
def test_embed_one_batch_yields_embeddings(mistral_models):
    for model in mistral_models:
        input_data = ["hello", "world"]

        embeddings = list(model._embed_one_batch(input_data))

        assert len(embeddings) == len(input_data)
        for emb in embeddings:
            assert isinstance(emb, list)
            assert all(isinstance(x, float) for x in emb)
