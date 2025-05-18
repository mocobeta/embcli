from typing import Iterator

import embcli_core
import torch
from embcli_core.models import LocalEmbeddingModel
from sentence_transformers import SentenceTransformer


class SentenceTransformerModel(LocalEmbeddingModel):
    vendor = "sbert"
    default_batch_size = 100
    model_aliases = [("sentence-transformers", ["sbert"])]
    valid_options = []
    local_model_list = "https://sbert.net/docs/sentence_transformer/pretrained_models.html"

    def __init__(self, model_id: str, **kwargs):
        super().__init__(model_id, **kwargs)
        if self.local_model_id is None:
            raise ValueError(
                "model id must contain actual SentenceTransformer model to be used. e.g. sentece-transformers/all-MiniLM-L6-v2"  # noqa: E501
            )
        device = "gpu" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(self.local_model_id, device=device)

    def _embed_one_batch(self, input: list[str], **kwargs) -> Iterator[list[float]]:
        if not input:
            return
        # Call SentencteTransformer to get embeddings
        embeddings = self.model.encode(input, **kwargs)
        for embedding in embeddings.tolist():
            yield embedding


@embcli_core.hookimpl
def embedding_model():
    def create(model_id: str, **kwargs):
        model_ids = [alias[0] for alias in SentenceTransformerModel.model_aliases]
        if model_id not in model_ids:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return SentenceTransformerModel(model_id, **kwargs)

    return SentenceTransformerModel, create
