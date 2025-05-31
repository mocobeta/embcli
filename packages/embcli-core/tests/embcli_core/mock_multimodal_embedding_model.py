import random
from typing import Iterator

import embcli_core
import numpy as np
from embcli_core.models import Modality, ModelOption, ModelOptionType, MultimodalEmbeddingModel


class MockMultimodalEmbeddingModel(MultimodalEmbeddingModel):
    vendor = "mock-multimodal"
    default_batch_size = 2
    model_aliases = [("multimodal-mock-1", ["mm-mock1"]), ("multimodal-mock-2", ["mm-mock2"])]
    valid_options = [
        ModelOption("option1", ModelOptionType.INT, "Model option 1"),
        ModelOption("option2", ModelOptionType.STR, "Model option 2"),
    ]

    def _embed_one_batch_multimodal(self, input: list[str], modality: Modality, **kwargs) -> Iterator[list[float]]:
        for _ in input:
            vector = [random.uniform(-1, 1) for _ in range(10)]
            vector = np.array(vector) / np.linalg.norm(vector)
            yield list(vector)


@embcli_core.hookimpl
def embedding_model():
    def create(model_id: str):
        if model_id not in ["multimodal-mock-1", "multimodal-mock-2"]:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return MockMultimodalEmbeddingModel(model_id)

    return MockMultimodalEmbeddingModel, create
