import os
from typing import Iterator

import embcli_core
from cohere import ClientV2
from embcli_core.models import EmbeddingModel, ModelOption, ModelOptionType


class CohereEmbeddingModel(EmbeddingModel):
    vendor = "cohere"
    default_batch_size = 50
    model_aliases = [
        ("embed-v4.0", ["embed-v4"]),
        ("embed-english-v3.0", ["embed-en-v3"]),
        ("embed-english-light-v3.0", ["embed-en-light-v3"]),
        ("embed-multilingual-v3.0", ["embed-multiling-v3"]),
        ("embed-multilingual-light-v3.0", ["embed-multiling-light-v3"]),
    ]
    valid_options = [
        ModelOption(
            "input_type",
            ModelOptionType.STR,
            "The type of input, affecting how the model processes it. Options include 'search_document', 'search_query', 'classification', 'clustering', 'image'.",  # noqa:　E501
        ),
        # ModelOption(
        #    "embedding_type",
        #    ModelOptionType.STR,
        #    "The type of embeddings to return. Options include 'float', 'int8', 'uint8', 'binary', 'ubinary'"
        # ),
        ModelOption(
            "truncate",
            ModelOptionType.STR,
            "How to handle text inputs that exceed the model's token limit. Options include 'none', 'start', 'end', 'middle'.",  # noqa: E501
        ),
    ]

    def __init__(self, model_id: str):
        super().__init__(model_id)
        self.client = ClientV2(api_key=os.environ.get("COHERE_API_KEY"))

    def _embed_one_batch(self, input: list[str], **kwargs) -> Iterator[list[float]]:
        if not input:
            return
        # Call Cohere API to get embeddings
        if "input_type" not in kwargs:
            kwargs["input_type"] = "search_document"
        response = self.client.embed(model=self.model_id, texts=input, embedding_types=["float"], **kwargs)

        assert response.embeddings.float_ is not None, "Cohere API returned no embeddings."

        for embedding in response.embeddings.float_:
            yield embedding

    def embed_batch_for_ingest(self, input, batch_size, **kwargs):
        kwargs["input_type"] = "search_document"
        return self.embed_batch(input, batch_size, **kwargs)

    def embed_for_search(self, input, **kwargs):
        kwargs["input_type"] = "search_query"
        return self.embed(input, **kwargs)


@embcli_core.hookimpl
def embedding_model():
    def create(model_id: str):
        model_ids = [alias[0] for alias in CohereEmbeddingModel.model_aliases]
        if model_id not in model_ids:
            raise ValueError(f"Model ID {model_id} is not supported.")
        return CohereEmbeddingModel(model_id)

    return CohereEmbeddingModel, create
