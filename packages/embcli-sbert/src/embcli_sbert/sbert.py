from typing import Iterator

import embcli_core
from embcli_core.models import EmbeddingModel
from sentence_transformers import SentenceTransformer


class SBERTEmbeddingModel(EmbeddingModel):
    vendor = "sbert"
    default_batch_size = 100
    model_aliases = [
        ("all-mpnet-base-v2", []),
        ("all-distilroberta-v1", []),
        ("all-MiniLM-L12-v2", []),
        ("all-MiniLM-L6-v2", []),
        ("multi-qa-distilbert-cos-v1", []),
        ("multi-qa-mpnet-base-dot-v1", []),
        ("multi-qa-MiniLM-L6-cos-v1", []),
        ("paraphrase-multilingual-mpnet-base-v2", []),
        ("paraphrase-multilingual-MiniLM-L12-v2", []),
        ("paraphrase-albert-small-v2", []),
        ("paraphrase-MiniLM-L3-v2", []),
        ("distiluse-base-multilingual-cased-v1", []),
        ("distiluse-base-multilingual-cased-v2", []),
    ]
    valid_options = []

    def __init__(self, model_id: str):
        super().__init__(model_id=model_id)
        self.model = SentenceTransformer(self.model_id)

    def _embed_one_batch(self, input: list[str], **kwargs) -> Iterator[list[float]]:
        if not input:
            return
        # Call SentencteTransformer to get embeddings
        embeddings = self.model.encode(input, **kwargs)
        for embedding in embeddings.tolist():
            yield embedding


@embcli_core.hookimpl
def embedding_model():
    def create(model_id: str):
        model_ids = [alias[0] for alias in SBERTEmbeddingModel.model_aliases]
        if model_id not in model_ids:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return SBERTEmbeddingModel(model_id)

    return SBERTEmbeddingModel, create
