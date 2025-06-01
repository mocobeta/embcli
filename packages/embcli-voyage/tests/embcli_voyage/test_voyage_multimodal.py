import os
from importlib.resources import files

import pytest
from embcli_core.models import Modality
from embcli_voyage.voyage_multimodal import VoyageMultimodalEmbeddingModel, embedding_model

skip_if_no_api_key = pytest.mark.skipif(
    not os.environ.get("VOYAGE_API_KEY") or not os.environ.get("RUN_VOYAGE_MM_TESTS") == "1",
    reason="VOYAGE_API_KEY and RUN_VOYAGE_MM_TESTS environment variables not set",
)


@skip_if_no_api_key
def test_factory_create_valid_multimodal_model():
    _, create = embedding_model()
    model = create("voyage-multimodal-3")
    assert isinstance(model, VoyageMultimodalEmbeddingModel)
    assert model.model_id == "voyage-multimodal-3"


@skip_if_no_api_key
def test_factory_create_invalid_multimodal_model():
    _, create = embedding_model()
    with pytest.raises(ValueError):
        create("invalid-multimodal-model-id")


@skip_if_no_api_key
def test_embed_one_batch_multimodal_text(voyage_multimodal_models):
    for model in voyage_multimodal_models:
        input_data = ["hello", "world"]

        embeddings = list(model._embed_one_batch_multimodal(input_data, Modality.TEXT))
        assert len(embeddings) == len(input_data)
        for emb in embeddings:
            assert isinstance(emb, list)
            assert all(isinstance(x, float) for x in emb)


@skip_if_no_api_key
def test_embed_one_batch_multimodal_image(voyage_multimodal_models):
    for model in voyage_multimodal_models:
        image_paths = [
            files("tests.embcli_voyage").joinpath("flying_cat.jpeg"),
            files("tests.embcli_voyage").joinpath("sleepy_sheep.jpeg"),
        ]
        input_data = [str(image_path) for image_path in image_paths]
        embeddings = list(model._embed_one_batch_multimodal(input_data, Modality.IMAGE))
        assert len(embeddings) == len(input_data)
        for emb in embeddings:
            assert isinstance(emb, list)
            assert all(isinstance(x, float) for x in emb)
