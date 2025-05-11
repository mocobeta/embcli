import os
from typing import Iterator

import embcli_core
from embcli_core.models import EmbeddingModel, ModelOption, ModelOptionType
from voyageai.client import Client


class VoyageEmbeddingModel(EmbeddingModel):
    vendor = "voyage"
    default_batch_size = 100
    model_aliases = [
        ("voyage-3-large", []),
        ("voyage-3", []),
        ("voyage-3-lite", []),
        ("voyage-code-3", []),
        ("voyage-finance-2", []),
        ("voyage-law-2", []),
        ("voyage-code-2", []),
    ]
    valid_options = [
        ModelOption(
            "input_type",
            ModelOptionType.STR,
            "Type of the input text. Options: 'None', 'query', 'document' Defaults to 'None'.",
        ),
        ModelOption(
            "truncation",
            ModelOptionType.BOOL,
            "Whether to truncate the input texts to fit within the context length. Defaults to True.",
        ),
        ModelOption(
            "output_dimension", ModelOptionType.INT, "The number of dimensions for resulting output embeddings. "
        ),
    ]

    def __init__(self, model_id: str):
        super().__init__(model_id)
        self.client = Client(api_key=os.environ.get("VOYAGE_API_KEY"))

    def _embed_one_batch(self, input: list[str], **kwargs) -> Iterator[list[float]]:
        if not input:
            return
        # Call Voyage API to get embeddings
        response = self.client.embed(model=self.model_id, texts=input, **kwargs)
        for embedding in response.embeddings:
            yield embedding  # type: ignore

    def embed_batch_for_ingest(self, input, batch_size, **kwargs):
        kwargs["input_type"] = "document"
        return self.embed_batch(input, batch_size, **kwargs)

    def embed_for_search(self, input, **kwargs):
        kwargs["input_type"] = "query"
        return self.embed(input, **kwargs)


@embcli_core.hookimpl
def embedding_model():
    def create(model_id: str):
        model_ids = [alias[0] for alias in VoyageEmbeddingModel.model_aliases]
        if model_id not in model_ids:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return VoyageEmbeddingModel(model_id)

    return VoyageEmbeddingModel, create
