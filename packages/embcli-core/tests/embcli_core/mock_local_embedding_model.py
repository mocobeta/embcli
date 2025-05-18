import random
from typing import Iterator

import embcli_core
import numpy as np
from embcli_core.models import LocalEmbeddingModel


class MockLocalEmbeddingModel(LocalEmbeddingModel):
    vendor = "mock-local"
    default_batch_size = 2
    model_aliases = [("local-embedding-mock", ["local-mock"])]
    valid_options = []
    local_model_list = "https://example.com/models.html"

    def _embed_one_batch(self, input: list[str], **kwargs) -> Iterator[list[float]]:
        for _ in input:
            vector = [random.uniform(-1, 1) for _ in range(10)]
            vector = np.array(vector) / np.linalg.norm(vector)
            yield list(vector)


@embcli_core.hookimpl
def embedding_model():
    def create(model_id: str, **kwargs):
        if model_id not in ["local-embedding-mock"]:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return MockLocalEmbeddingModel(model_id, **kwargs)

    return MockLocalEmbeddingModel, create
