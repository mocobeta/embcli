import os
from importlib.resources import files

import pytest
from embcli_clip.clip import CLIPModel, embedding_model
from embcli_core.models import Modality

skip_if_no_envvar_to_run = pytest.mark.skipif(
    not os.environ.get("RUN_CLIP_TESTS") == "1",
    reason="RUN_CLIP_TESTS environment variable not set",
)


@skip_if_no_envvar_to_run
def test_initialize_model_default_local_model_id():
    _, create = embedding_model()
    model = create("clip")
    assert isinstance(model, CLIPModel)
    assert model.model_id == "clip"
    assert model.local_model_id == "openai/clip-vit-base-patch32"


@skip_if_no_envvar_to_run
def test_factory_create_valid_model():
    _, create = embedding_model()
    kwargs = {"local_model_id": "openai/clip-vit-base-patch16"}
    model = create("clip", **kwargs)
    assert isinstance(model, CLIPModel)
    assert model.model_id == "clip"
    assert model.local_model_id == "openai/clip-vit-base-patch16"


@skip_if_no_envvar_to_run
def test_factory_create_invalid_model():
    _, create = embedding_model()
    with pytest.raises(ValueError):
        create("invalid-model-id")


@skip_if_no_envvar_to_run
def test_embed_one_batch_multimoda_text(clip_model):
    model = clip_model
    input_data = ["hello", "world"]

    embeddings = list(model._embed_one_batch_multimodal(input_data, Modality.TEXT))

    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert isinstance(emb, list)
        assert all(isinstance(x, float) for x in emb)


@skip_if_no_envvar_to_run
def test_embed_one_batch_multimodal_image(clip_model):
    model = clip_model
    image_paths = [
        files("tests.embcli_clip").joinpath("flying_cat.jpeg"),
        files("tests.embcli_clip").joinpath("sleepy_sheep.jpeg"),
    ]
    input_data = [str(image_path) for image_path in image_paths]
    embeddings = list(model._embed_one_batch_multimodal(input_data, Modality.IMAGE))
    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert isinstance(emb, list)
        assert all(isinstance(x, float) for x in emb)
