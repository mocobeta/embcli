import os
from typing import Iterator, List

import embcli_core
from embcli_core.models import EmbeddingModel, ModelOption, ModelOptionType
from google import genai
from google.genai import types


class GeminiEmbeddingModel(EmbeddingModel):
    vendor = "gemini"
    default_batch_size = 100
    model_aliases = [
        ("gemini-embedding-exp-03-07", ["exp-03-07"]),
        ("text-embedding-004", ["text-004"]),
        ("embedding-001", []),
    ]
    valid_options = [
        ModelOption(
            "task_type",
            ModelOptionType.STR,
            "The type of task for the embedding. See https://ai.google.dev/gemini-api/docs/embeddings#task-types for supported task types.",  # noqa: E501
        )
    ]

    def __init__(self, model_id: str):
        self.model_id = model_id
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    def _embed_one_batch(self, input: List[str], **kwargs) -> Iterator[List[float]]:
        if not input:
            return
        # Call Gemini API to get embeddings
        if kwargs.get("task_type") is None:
            config = None
        else:
            config = types.EmbedContentConfig(task_type=kwargs.get("task_type"))
        response = self.client.models.embed_content(
            model=self.model_id,
            contents=input,
            config=config,
        )
        if not response.embeddings:
            return
        for embedding in response.embeddings:
            while embedding.values is None:
                continue
            yield embedding.values


@embcli_core.hookimpl
def embedding_model():
    def create(model_id: str):
        model_ids = [alias[0] for alias in GeminiEmbeddingModel.model_aliases]
        if model_id not in model_ids:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return GeminiEmbeddingModel(model_id)

    return GeminiEmbeddingModel, create
