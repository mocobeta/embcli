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
def test_initialize_model_no_local_model_id():
    _, create = embedding_model()
    with pytest.raises(ValueError):
        create("sentence-transformers")


@skip_if_no_envvar_to_run
def test_embed_one_batch_yields_embeddings(sbert_model):
    model = sbert_model
    input_data = ["hello", "world"]

    embeddings = list(model._embed_one_batch(input_data))

    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert isinstance(emb, list)
        assert all(isinstance(x, float) for x in emb)
