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
        ModelOption(
            "embedding_type",
            ModelOptionType.STR,
            "The type of embeddings to return. Options include 'float', 'int8', 'uint8', 'binary', 'ubinary'",
        ),
        ModelOption(
            "truncate",
            ModelOptionType.STR,
            "How to handle text inputs that exceed the model's token limit. Options include 'none', 'start', 'end', 'middle'.",  # noqa: E501
        ),
    ]

    def __init__(self, model_id: str):
        super().__init__(model_id)
        self.client = ClientV2(api_key=os.environ.get("COHERE_API_KEY"))

    def _embed_one_batch(self, input: list[str], **kwargs) -> Iterator[list[float] | list[int]]:
        if not input:
            return
        # Call Cohere API to get embeddings
        if "input_type" not in kwargs:
            kwargs["input_type"] = "search_document"
        if "embedding_type" in kwargs:
            # Cohere API expects embedding types in a list
            embedding_type = kwargs["embedding_type"]
            del kwargs["embedding_type"]
        else:
            embedding_type = "float"
        response = self.client.embed(model=self.model_id, texts=input, embedding_types=[embedding_type], **kwargs)

        match embedding_type:
            case "float":
                assert response.embeddings.float_ is not None, "Cohere API returned no embeddings."
                for embedding in response.embeddings.float_:
                    yield embedding
            case "int8":
                assert response.embeddings.int8 is not None, "Cohere API returned no embeddings."
                for embedding in response.embeddings.int8:
                    yield embedding
            case "uint8":
                assert response.embeddings.uint8 is not None, "Cohere API returned no embeddings."
                for embedding in response.embeddings.uint8:
                    yield embedding
            case "binary":
                assert response.embeddings.binary is not None, "Cohere API returned no embeddings."
                for embedding in response.embeddings.binary:
                    yield embedding
            case "ubinary":
                assert response.embeddings.ubinary is not None, "Cohere API returned no embeddings."
                for embedding in response.embeddings.ubinary:
                    yield embedding
            case _:
                raise ValueError(
                    f"Unsupported embedding type: {embedding_type}. Supported types are 'float', 'int8', 'uint8', 'binary', 'ubinary'."  # noqa: E501
                )

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
