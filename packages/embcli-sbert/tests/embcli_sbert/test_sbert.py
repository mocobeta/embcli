import pytest
from embcli_sbert.sbert import SBERTEmbeddingModel, embedding_model


def test_factory_create_valid_model():
    _, create = embedding_model()
    model = create("all-MiniLM-L6-v2")
    assert isinstance(model, SBERTEmbeddingModel)
    assert model.model_id == "all-MiniLM-L6-v2"


def test_factory_create_invalid_model():
    _, create = embedding_model()
    with pytest.raises(ValueError):
        create("invalid-model-id")


def test_embed_one_batch_yields_embeddings(sbert_model):
    model = sbert_model
    input_data = ["hello", "world"]

    embeddings = list(model._embed_one_batch(input_data))

    assert len(embeddings) == len(input_data)
    for emb in embeddings:
        assert isinstance(emb, list)
        assert all(isinstance(x, float) for x in emb)
