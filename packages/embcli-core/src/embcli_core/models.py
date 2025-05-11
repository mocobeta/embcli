from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Iterator, Optional, Type


class ModelOptionType(Enum):
    BOOL = "bool"
    INT = "int"
    FLOAT = "float"
    STR = "str"


@dataclass
class ModelOption:
    name: str
    type: ModelOptionType
    description: str = ""


class EmbeddingModel(ABC):
    """Abstract base class for embedding models."""

    vendor: str
    default_batch_size: int
    model_aliases: list[tuple[str, list[str]]]
    valid_options: list[ModelOption]

    def __init__(self, model_id: str):
        self.model_id = model_id

    def __str__(self):
        return f"{self.__class__.__name__}(vendor={self.vendor}, model_id={self.model_id})"

    def embed(self, input: str, **kwargs) -> list[float]:
        """Generate an embedding for a single input.
        Args:
            input (str): The input string to embed.
            **kwargs: Additional keyword arguments for the embedding model.
        Returns:
            list[float]: The generated embedding.
        """
        model_options = self._check_and_convert_options(**kwargs)
        return next(self._embed_one_batch([input], **model_options))

    def embed_for_search(self, input: str, **kwargs) -> list[float]:
        """Generate an embedding for a single input. Output is supposed to be used for search query."""
        # This method is a placeholder and can be overridden by subclasses if needed.
        return self.embed(input, **kwargs)

    def embed_batch(self, input: list[str], batch_size: Optional[int], **kwargs) -> Iterator[list[float]]:
        """Generate embeddings for a list of inputs. Inputs are split into batches of size `batch_size`.
        Args:
            input (list[str]): The list of input strings to embed.
            batch_size (Optional[int]): The size of each batch. If None, the default batch size is used.
            **kwargs: Additional keyword arguments for the embedding model.
        Returns:
            Iterator[list[float]]: An iterator that yields the generated embeddings for each batch.
        """
        model_options = self._check_and_convert_options(**kwargs)
        if not input:
            return iter([])
        if batch_size is None:
            batch_size = self.default_batch_size
        for i in range(0, len(input), batch_size):
            yield from self._embed_one_batch(input[i : i + batch_size], **model_options)

    def embed_batch_for_ingest(self, input: list[str], batch_size: Optional[int], **kwargs) -> Iterator[list[float]]:
        """Generate embeddings for a list of inputs. Outputs are supposed to be used for ingestion."""
        # This method is a placeholder and can be overridden by subclasses if needed.
        return self.embed_batch(input, batch_size, **kwargs)

    @abstractmethod
    def _embed_one_batch(self, input: list[str], **kwargs) -> Iterator[list[float]]:
        """Generate embeddings for a batch of inputs."""

    def _check_and_convert_options(self, **kwargs) -> dict[str, Any]:
        converted_options = {}
        for option in self.valid_options:
            if option.name in kwargs:
                value = kwargs[option.name]
                try:
                    if option.type == ModelOptionType.BOOL:
                        converted_options[option.name] = bool(value)
                    elif option.type == ModelOptionType.INT:
                        converted_options[option.name] = int(value)
                    elif option.type == ModelOptionType.FLOAT:
                        converted_options[option.name] = float(value)
                    elif option.type == ModelOptionType.STR:
                        converted_options[option.name] = str(value)
                except ValueError:
                    raise ValueError(f"Invalid option value type: {value} for {option.name}")
        return converted_options


__models: dict[str, Type[EmbeddingModel]] = {}
__model_factories: dict[str, Callable[[str], EmbeddingModel]] = {}
__model_aliases: dict[str, str] = {}


def register(model_cls: Type[EmbeddingModel], factory: Callable[[str], EmbeddingModel]):
    """Register an embedding model.
    Args:
        model_cls: The embedding model class to register.
        factory: A factory function that creates an instance of the model.
    """
    for model_id, aliases in model_cls.model_aliases:
        __models[model_id] = model_cls
        __model_factories[model_id] = factory
        for alias in aliases:
            __model_aliases[alias] = model_id


def avaliable_models() -> list[Type[EmbeddingModel]]:
    """Get a list of available model IDs.
    Returns:
        list[str]: A list of model IDs.
    """
    return list(set(__models.values()))


def get_model(model_id_or_alias: str) -> Optional[EmbeddingModel]:
    """Get a model class by its ID or alias.
    Args:
        model_id_or_alias (str): The model ID or alias.
    Returns:
        Optional[EmbeddingModel]: The model class, or None if not found.
    """
    model_id: str
    if model_id_or_alias in __models:
        model_id = model_id_or_alias
    elif model_id_or_alias in __model_aliases:
        model_id = __model_aliases[model_id_or_alias]
    else:
        return None

    assert model_id in __model_factories
    factory = __model_factories[model_id]
    return factory(model_id)
