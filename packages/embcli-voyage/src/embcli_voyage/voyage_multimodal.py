import os
from typing import Iterator

import embcli_core
from embcli_core.models import Modality, ModelOption, ModelOptionType, MultimodalEmbeddingModel
from PIL import Image
from voyageai.client import Client


class VoyageMultimodalEmbeddingModel(MultimodalEmbeddingModel):
    vendor = "voyage"
    default_batch_size = 100
    model_aliases = [("voyage-multimodal-3", ["voyage-mm-3"])]
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
    ]

    def __init__(self, model_id: str):
        super().__init__(model_id)
        self.client = Client(api_key=os.environ.get("VOYAGE_API_KEY"))

    def _embed_one_batch_multimodal(self, input: list[str], modality: Modality, **kwargs) -> Iterator[list[float]]:
        if not input:
            return
        match modality:
            case Modality.TEXT:
                inputs = [[text] for text in input]
            case Modality.IMAGE:
                inputs = [[Image.open(img_path)] for img_path in input]
            case _:
                raise ValueError(f"Unsupported modality: {modality}")
        # Call Voyage API to get embeddings
        response = self.client.multimodal_embed(inputs=inputs, model=self.model_id, **kwargs)  # type: ignore
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
        model_ids = [alias[0] for alias in VoyageMultimodalEmbeddingModel.model_aliases]
        if model_id not in model_ids:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return VoyageMultimodalEmbeddingModel(model_id)

    return VoyageMultimodalEmbeddingModel, create
