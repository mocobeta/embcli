import os
from typing import Iterator

import embcli_core
from embcli_core.models import EmbeddingModel, ModelOption, ModelOptionType
from mistralai import Mistral


class MistralEmbeddingModel(EmbeddingModel):
    vendor = "mistral"
    default_batch_size = 100
    model_aliases = [("mistral-embed", []), ("codestral-embed", [])]
    valid_options = [
        ModelOption(
            name="output_dimension",
            type=ModelOptionType.INT,
            description="The dimesions of the output embedding, defaults to 1536 and has a maximum value of 3072. Only supprted in codestral-embed model.",  # noqa: E501
        )
    ]

    def __init__(self, model_id: str):
        super().__init__(model_id)
        self.client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))

    def _embed_one_batch(self, input: list[str], **kwargs) -> Iterator[list[float]]:
        if not input:
            return
        # Call Mistral API to get embeddings
        response = self.client.embeddings.create(model=self.model_id, inputs=input, **kwargs)
        for item in response.data:
            yield item.embedding if item.embedding else []


@embcli_core.hookimpl
def embedding_model():
    def create(model_id: str):
        model_ids = [alias[0] for alias in MistralEmbeddingModel.model_aliases]
        if model_id not in model_ids:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return MistralEmbeddingModel(model_id)

    return MistralEmbeddingModel, create
