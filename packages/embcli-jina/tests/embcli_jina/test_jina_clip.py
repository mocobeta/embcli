import os
from importlib.resources import files

import pytest
from embcli_core.models import Modality
from embcli_jina.jina_clip import JinaClipModel, embedding_model

skip_if_no_api_key = pytest.mark.skipif(
    not os.environ.get("JINA_API_KEY") or not os.environ.get("RUN_JINA_CLIP_TESTS") == "1",
    reason="JINA_API_KEY and RUN_JINA_CLIP_TESTS environment variables not set",
)


@skip_if_no_api_key
def test_factory_create_valid_model():
    _, create = embedding_model()
    model = create("jina-clip-v2")
    assert isinstance(model, JinaClipModel)
    assert model.model_id == "jina-clip-v2"
    assert model.endpoint == "https://api.jina.ai/v1/embeddings"


@skip_if_no_api_key
def test_factory_create_invalid_model():
    _, create = embedding_model()
    with pytest.raises(ValueError):
        create("invalid-model-id")


@skip_if_no_api_key
def test_embed_one_batch_multimodal(jina_clip_models):
    for model in jina_clip_models:
        print(f"Testing model: {model.model_id}")
        input_data = ["hello", "world"]

        embeddings = list(model._embed_one_batch_multimodal(input_data, modality=Modality.TEXT))

        assert len(embeddings) == len(input_data)
        for emb in embeddings:
            assert isinstance(emb, list)
            assert all(isinstance(x, float) for x in emb)


@skip_if_no_api_key
def test_embed_one_batch_multimodal_image(jina_clip_models):
    for model in jina_clip_models:
        image_paths = [
            files("tests.embcli_jina").joinpath("flying_cat.jpeg"),
            files("tests.embcli_jina").joinpath("sleepy_sheep.jpeg"),
        ]
        input_data = [str(image_path) for image_path in image_paths]
        embeddings = list(model._embed_one_batch_multimodal(input_data, Modality.IMAGE))
        assert len(embeddings) == len(input_data)
        for emb in embeddings:
            assert isinstance(emb, list)
            assert all(isinstance(x, float) for x in emb)
            assert len(emb) == 1024


@skip_if_no_api_key
def test_embed_batch_with_options(jina_clip_models):
    input_data = ["hello", "world"]
    for model in jina_clip_models:
        options = {"task": "retrieval.query", "dimensions": 512}
        embeddings = list(model.embed_batch(input_data, None, **options))
        assert len(embeddings) == len(input_data)
        for emb in embeddings:
            assert isinstance(emb, list)
            assert all(isinstance(x, float) for x in emb)
            assert len(emb) == 512
