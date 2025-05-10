import os
from typing import Iterator

import embcli_core
from embcli_core.models import EmbeddingModel, ModelOption, ModelOptionType
from openai import OpenAI


class OpenAIEmbeddingModel(EmbeddingModel):
    vendor = "openai"
    default_batch_size = 100
    model_aliases = [
        ("text-embedding-3-small", ["3-small"]),
        ("text-embedding-3-large", ["3-large"]),
        ("text-embedding-ada-002", ["ada-002"]),
    ]
    valid_options = [
        ModelOption(
            "dimensions",
            ModelOptionType.INT,
            "The number of dimensions the resulting output embeddings should have. Only supported in text-embedding-3 and later models.",  # noqa: E501
        )
    ]

    def __init__(self, model_id: str):
        super().__init__(model_id)
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))  # type: ignore

    def _embed_one_batch(self, input: list[str], **kwargs) -> Iterator[list[float]]:
        if not input:
            return
        # Call OpenAI API to get embeddings
        response = self.client.embeddings.create(
            model=self.model_id,
            input=input,
            **kwargs,
        )
        for item in response.data:
            yield item.embedding


@embcli_core.hookimpl
def embedding_model():
    def create(model_id: str):
        model_ids = [alias[0] for alias in OpenAIEmbeddingModel.model_aliases]
        if model_id not in model_ids:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return OpenAIEmbeddingModel(model_id)

    return OpenAIEmbeddingModel, create
