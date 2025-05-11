import os
from typing import Iterator

import embcli_core
import httpx
from embcli_core.models import EmbeddingModel, ModelOption, ModelOptionType

COLBERT_TIMEOUT_SEC = 5  # Timeout for ColBERT model requests


class JinaEmbeddingModel(EmbeddingModel):
    vendor = "jina"
    default_batch_size = 100
    model_aliases = [
        ("jina-embeddings-v3", ["jina-v3"]),
        ("jina-colbert-v2", ["colbert-v2"]),
        ("jina-embeddings-v2-base-code", ["jina-v2-code"]),
    ]
    model_endoints = {
        "jina-embeddings-v3": "https://api.jina.ai/v1/embeddings",
        "jina-colbert-v2": "https://api.jina.ai/v1/multi-vector",
        "jina-embeddings-v2-base-code": "https://api.jina.ai/v1/embeddings",
    }
    valid_options = [
        ModelOption(
            "task",
            ModelOptionType.STR,
            "Downstream task for which the embeddings are used. Supported tasks: 'text-matching', 'retrieval.query', 'retrieval.passage', 'separation', 'classification'. Only supported in jina-embeddings-v3.",  # noqa: E501
        ),
        ModelOption(
            "late_chunking",
            ModelOptionType.BOOL,
            "Whether if the late chunking is applied. Only supported in jina-embeddings-v3.",
        ),
        ModelOption(
            "truncate",
            ModelOptionType.BOOL,
            "When enabled, the model will automatically drop the tail that extends beyond the maximum context length allowed by the model instead of throwing an error. Only supported in jina-embeddings-v3.",  # noqa: E501
        ),
        ModelOption(
            "dimensions",
            ModelOptionType.INT,
            "The number of dimensions the resulting output embeddings should have. Only supported in jina-embeddings-v3 and jina-colbert-v2.",  # noqa: E501
        ),
        ModelOption(
            "input_type",
            ModelOptionType.STR,
            "The type of input to the model. Supported types: 'query', 'document' Only supported in jina-corebert-v2.",
        ),
    ]

    def __init__(self, model_id):
        super().__init__(model_id)
        self.endpoint = self.model_endoints[model_id]
        self.api_key = os.environ.get("JINA_API_KEY")

    def _embed_one_batch(self, input: list[str], **kwargs) -> Iterator[list[float]]:
        if not input:
            return
        # Call Jina API to get embeddings
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
        data = {"model": self.model_id, "input": input}
        if self.model_id == "jina-embeddings-v3":
            data["task"] = kwargs.get("task", "text-matching")
            if "late_chunking" in kwargs:
                data["late_chunking"] = kwargs["late_chunking"]
            if "truncate" in kwargs:
                data["truncate"] = kwargs["truncate"]
            if "dimensions" in kwargs:
                data["dimensions"] = kwargs["dimensions"]
        elif self.model_id == "jina-colbert-v2":
            if "input_type" in kwargs:
                data["input_type"] = kwargs["input_type"]
            if "dimensions" in kwargs:
                data["dimensions"] = kwargs["dimensions"]

        timeout = COLBERT_TIMEOUT_SEC if self.model_id == "jina-colbert-v2" else None
        response = httpx.post(self.endpoint, headers=headers, json=data, timeout=timeout)
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
        if self.model_id == "jina-embeddings-v3":
            kwargs["task"] = "retrieval.passage"
        elif self.model_id == "jina-colbert-v2":
            kwargs["input_type"] = "document"
        return self.embed_batch(input, batch_size, **kwargs)

    def embed_for_search(self, input, **kwargs):
        if self.model_id == "jina-embeddings-v3":
            kwargs["task"] = "retrieval.query"
        elif self.model_id == "jina-colbert-v2":
            kwargs["input_type"] = "query"
        return self.embed(input, **kwargs)


@embcli_core.hookimpl
def embedding_model():
    def create(model_id: str):
        model_ids = [alias[0] for alias in JinaEmbeddingModel.model_aliases]
        if model_id not in model_ids:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return JinaEmbeddingModel(model_id)

    return JinaEmbeddingModel, create
