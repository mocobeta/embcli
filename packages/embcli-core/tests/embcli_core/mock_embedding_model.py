import random
from typing import Iterator

import embcli_core
import numpy as np
from embcli_core.models import EmbeddingModel, ModelOption, ModelOptionType


class MockEmbeddingModel(EmbeddingModel):
    vendor = "mock"
    default_batch_size = 2
    model_aliases = [("embedding-mock-1", ["mock1"]), ("embedding-mock-2", ["mock2"])]
    valid_options = [
        ModelOption("option1", ModelOptionType.INT, "Model option 1"),
        ModelOption("option2", ModelOptionType.STR, "Model option 2"),
    ]

    def _embed_one_batch(self, input: list[str], **kwargs) -> Iterator[list[float]]:
        for _ in input:
            vector = [random.uniform(-1, 1) for _ in range(10)]
            vector = np.array(vector) / np.linalg.norm(vector)
            yield list(vector)


@embcli_core.hookimpl
def embedding_model():
    def create(model_id: str):
        if model_id not in ["embedding-mock-1", "embedding-mock-2"]:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return MockEmbeddingModel(model_id)

    return MockEmbeddingModel, create
