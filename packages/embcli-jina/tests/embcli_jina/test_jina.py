import os

import pytest
from embcli_jina.jina import JinaEmbeddingModel, embedding_model

skip_if_no_api_key = pytest.mark.skipif(
    not os.environ.get("JINA_API_KEY") or not os.environ.get("RUN_JINA_TESTS") == "1",
    reason="JINA_API_KEY and RUN_JINA_TESTS environment variables not set",
)


@skip_if_no_api_key
def test_factory_create_valid_model():
    _, create = embedding_model()
    model = create("jina-embeddings-v3")
    assert isinstance(model, JinaEmbeddingModel)
    assert model.model_id == "jina-embeddings-v3"
    assert model.endpoint == "https://api.jina.ai/v1/embeddings"


@skip_if_no_api_key
def test_factory_create_invalid_model():
    _, create = embedding_model()
    with pytest.raises(ValueError):
        create("invalid-model-id")


@skip_if_no_api_key
def test_embed_one_batch_yields_embeddings(jina_models):
    for model in jina_models:
        print(f"Testing model: {model.model_id}")
        input_data = ["hello", "world"]

        embeddings = list(model._embed_one_batch(input_data))

        if "colbert" not in model.model_id:
            # Check if the length of the embeeddings matches the input data if the model is not colbert (multi-vectors)
            assert len(embeddings) == len(input_data)
        for emb in embeddings:
            assert isinstance(emb, list)
            assert all(isinstance(x, float) for x in emb)


@skip_if_no_api_key
def test_embed_batch_with_options(jina_models):
    input_data = ["hello", "world"]
    for model in jina_models:
        if model.model_id == "jina-embeddings-v3":
            options = {"task": "retrieval.passage", "late_chunking": True, "truncate": True, "dimensions": "512"}

            embeddings = list(model.embed_batch(input_data, None, **options))

            assert len(embeddings) == len(input_data)
            for emb in embeddings:
                assert isinstance(emb, list)
                assert all(isinstance(x, float) for x in emb)
                assert len(emb) == 512
