import os

import pytest
from embcli_llamacpp import llamacpp
from embcli_llamacpp.llamacpp import embedding_model

skip_if_no_envvar_to_run = pytest.mark.skipif(
    not os.environ.get("RUN_LLAMA_TESTS") == "1",
    reason="RUN_LLAMA_TESTS environment variable not set",
)


@skip_if_no_envvar_to_run
def test_factory_create_valid_model(test_model_file):
    _, create = embedding_model()
    kwargs = {"local_model_path": test_model_file}
    model = create("llama-cpp", **kwargs)
    assert isinstance(model, llamacpp.LlamaCppModel)
    assert model.vendor == "llama-cpp"
    assert model.model_id == "llama-cpp"
    assert model.local_model_path == test_model_file


@skip_if_no_envvar_to_run
def test_factory_create_invalid_model():
    _, create = embedding_model()
    with pytest.raises(ValueError):
        create("invalid-model-id")


@skip_if_no_envvar_to_run
def test_factory_create_invalid_model_path():
    _, create = embedding_model()
    with pytest.raises(ValueError):
        create("llama-cpp", local_model_path="invalid/path/to/model")


@skip_if_no_envvar_to_run
def test_embed_one_batch_yields_embeddings(llamacpp_model):
    model = llamacpp_model
    input_data = ["hello", "world"]

    embeddings = list(model._embed_one_batch(input_data))

    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert isinstance(emb, list)
        assert all(isinstance(x, float) for x in emb)
