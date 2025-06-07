import os

import pytest
from embcli_sbert.sbert import SentenceTransformerModel, embedding_model

skip_if_no_envvar_to_run = pytest.mark.skipif(
    not os.environ.get("RUN_SBERT_TESTS") == "1",
    reason="RUN_SBERT_TESTS environment variable not set",
)


@skip_if_no_envvar_to_run
def test_factory_create_valid_model():
    _, create = embedding_model()
    kwargs = {"local_model_id": "all-MiniLM-L6-v2"}
    model = create("sentence-transformers", **kwargs)
    assert isinstance(model, SentenceTransformerModel)
    assert model.model_id == "sentence-transformers"
    assert model.local_model_id == "all-MiniLM-L6-v2"


@skip_if_no_envvar_to_run
def test_factory_create_invalid_model():
    _, create = embedding_model()
    with pytest.raises(ValueError):
        create("invalid-model-id")


@skip_if_no_envvar_to_run
def test_initialize_model_default_local_model_id():
    _, create = embedding_model()
    model = create("sentence-transformers")
    assert isinstance(model, SentenceTransformerModel)
    assert model.model_id == "sentence-transformers"
    assert model.local_model_id == "all-MiniLM-L6-v2"


@skip_if_no_envvar_to_run
def test_embed_one_batch_yields_embeddings(sbert_model):
    model = sbert_model
    input_data = ["hello", "world"]

    embeddings = list(model._embed_one_batch(input_data))

    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert isinstance(emb, list)
        assert all(isinstance(x, float) for x in emb)


@skip_if_no_envvar_to_run
def test_embed_batch_with_options(sbert_model):
    model = sbert_model
    input_data = ["hello", "world"]
    options = {"normalize_embeddings": True}

    embeddings = list(model.embed_batch(input_data, None, **options))

    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert isinstance(emb, list)
        assert all(isinstance(x, float) for x in emb)


@skip_if_no_envvar_to_run
def test_embed_batch_with_precision(sbert_model):
    model = sbert_model
    input_data = ["hello", "world"]

    # Test with int8 precision
    options = {"precision": "int8"}
    embeddings = list(model.embed_batch(input_data, None, **options))
    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert isinstance(emb, list)
        assert all(isinstance(x, int) for x in emb)
        assert all(-128 <= x <= 127 for x in emb)

    # Test with uint8 precision
    options = {"precision": "uint8"}
    embeddings = list(model.embed_batch(input_data, None, **options))
    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert isinstance(emb, list)
        assert all(isinstance(x, int) for x in emb)
        assert all(0 <= x <= 255 for x in emb)

    # Test with binary precision
    options = {"precision": "binary"}
    embeddings = list(model.embed_batch(input_data, None, **options))
    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert isinstance(emb, list)
        assert all(isinstance(x, int) for x in emb)
        assert all(-128 <= x <= 127 for x in emb)

    # Test with ubinary precision
    options = {"precision": "ubinary"}
    embeddings = list(model.embed_batch(input_data, None, **options))
    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert isinstance(emb, list)
        assert all(isinstance(x, int) for x in emb)
        assert all(0 <= x <= 255 for x in emb)
