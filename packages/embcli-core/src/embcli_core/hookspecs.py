from typing import Callable, Type

import pluggy

from .models import EmbeddingModel

hookspec = pluggy.HookspecMarker("embcli")
hookimpl = pluggy.HookimplMarker("embcli")


@hookspec
def embedding_model() -> tuple[Type[EmbeddingModel], Callable[[str], EmbeddingModel]]:  # type: ignore
    """Hook to register an embedding model.
    Returns:
        tuple: A tuple containing the model class and a factory function.
    """
