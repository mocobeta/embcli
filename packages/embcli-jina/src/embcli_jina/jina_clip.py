import base64
import os
from typing import Iterator

import embcli_core
import httpx
from embcli_core.models import Modality, ModelOption, ModelOptionType, MultimodalEmbeddingModel


def image_to_base64(image_path: str) -> str:
    """Encodes an image file to a base64 string."""
    with open(image_path, "rb") as image_file:
        data = base64.b64encode(image_file.read())
    return data.decode("utf-8")


class JinaClipModel(MultimodalEmbeddingModel):
    vendor = "jina"
    default_batch_size = 100
    model_aliases = [("jina-clip-v2", [])]
    valid_options = [
        ModelOption(
            "task",
            ModelOptionType.STR,
            "Downstream task for which the embeddings are used. Supported tasks: 'retrieval.query', 'retrieval.passage'.",  # noqa: E501
        ),
        ModelOption(
            "dimensions",
            ModelOptionType.INT,
            "The number of dimensions the resulting output embeddings should have.",
        ),
    ]

    def __init__(self, model_id: str, **kwargs):
        super().__init__(model_id, **kwargs)
        self.endpoint = "https://api.jina.ai/v1/embeddings"
        self.api_key = os.environ.get("JINA_API_KEY")

    def _embed_one_batch_multimodal(self, input: list[str], modality: Modality, **kwargs) -> Iterator[list[float]]:
        if not input:
            return

        # Call Jina API to get embeddings
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
        data = {"model": self.model_id}
        match modality:
            case Modality.TEXT:
                data["input"] = [{"text": text} for text in input]  # type: ignore
            case Modality.IMAGE:
                data["input"] = [{"image": image_to_base64(image_path)} for image_path in input]  # type: ignore
            case _:
                raise ValueError(f"Unsupported modality: {modality}")
        if "task" in kwargs:
            data["task"] = kwargs["task"]
        if "dimensions" in kwargs:
            data["dimensions"] = kwargs["dimensions"]

        response = httpx.post(self.endpoint, headers=headers, json=data)
        response.raise_for_status()
        for item in response.json().get("data", []):
            if "embedding" in item:
                # single embedding
                yield item["embedding"]
            else:
                # multiple embeddings
                for embedding in item.get("embeddings", []):
                    yield embedding

    def embed_batch_for_ingest(self, input, batch_size, **kwargs):
        kwargs["task"] = "retrieval.passage"
        return self.embed_batch(input, batch_size, **kwargs)

    def embed_for_search(self, input, **kwargs):
        kwargs["task"] = "retrieval.query"
        return self.embed(input, **kwargs)


@embcli_core.hookimpl
def embedding_model():
    def create(model_id: str, **kwargs):
        model_ids = [alias[0] for alias in JinaClipModel.model_aliases]
        if model_id not in model_ids:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return JinaClipModel(model_id, **kwargs)

    return JinaClipModel, create
