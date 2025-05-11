import os
from typing import Iterator

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
            "The type of task for the embedding. Supported task types: 'semantic_similarity', 'classification', 'clustering', 'retrieval_document', 'retrieval_query', 'question_answering', 'fact_verification', 'code_retrieval_query'",  # noqa: E501
        )
    ]

    def __init__(self, model_id: str):
        self.model_id = model_id
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    def _embed_one_batch(self, input: list[str], **kwargs) -> Iterator[list[float]]:
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
            yield embedding.values if embedding.values else []

    def embed_batch_for_ingest(self, input, batch_size, **kwargs):
        kwargs["task_type"] = "retrieval_document"
        return self.embed_batch(input, batch_size, **kwargs)

    def embed_for_search(self, input, **kwargs):
        kwargs["task_type"] = "retrieval_query"
        return self.embed(input, **kwargs)


@embcli_core.hookimpl
def embedding_model():
    def create(model_id: str):
        model_ids = [alias[0] for alias in GeminiEmbeddingModel.model_aliases]
        if model_id not in model_ids:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return GeminiEmbeddingModel(model_id)

    return GeminiEmbeddingModel, create
