from typing import Callable, Type

import pluggy

from .models import EmbeddingModel
from .vector_stores import VectorStore

hookspec = pluggy.HookspecMarker("embcli")
hookimpl = pluggy.HookimplMarker("embcli")


@hookspec
def embedding_model() -> tuple[Type[EmbeddingModel], Callable[[str], EmbeddingModel]]:  # type: ignore
    """Hook to register an embedding model.
    Returns:
        tuple: A tuple containing the model class and a factory function.
    """


@hookspec
def vector_store() -> tuple[Type[VectorStore], Callable[[dict], VectorStore]]:  # type: ignore
    """Hook to register a vector store.
    Returns:
        tuple: A tuple containing the vector store class and a factory function.
    """
