from abc import ABC, abstractmethod
from typing import Callable, Iterator, Optional, TypeVar

from .document import DocumentType, HitDocument
from .models import EmbeddingModel, MultimodalEmbeddingModel

T = TypeVar("T")


class VectorStore(ABC):
    """Abstract base class for vector stores."""

    vendor: str

    def _batch(self, items: list[T], batch_size: int) -> Iterator[list[T]]:
        """
        Split items into batches of specified size.
        """
        for i in range(0, len(items), batch_size):
            yield items[i : i + batch_size]

    def ingest(self, model: EmbeddingModel, collection: str, docs: list[DocumentType], batch_size: int = 100, **kwargs):
        """Ingest documents into the collection.
        Ingestion-specific embeddings are used if the model provides options for generating search documents-optimized embeddings."""  # noqa: E501
        if not docs:
            return
        # Process documents in batches
        for batch_docs in self._batch(docs, batch_size):
            batch_input = [doc.source_text() for doc in batch_docs]
            # Generate embeddings for the batch
            embeddings = list(model.embed_batch_for_ingest(batch_input, batch_size=batch_size, **kwargs))
            # Index the embeddings with documents
            self._index(collection, embeddings, batch_docs)

    @abstractmethod
    def _index(self, collection: str, embeddings: list[list[float]], docs: list[DocumentType]):
        """Index the embeddings with documents."""
        pass

    def search(self, model: EmbeddingModel, collection: str, query: str, top_k: int = 5, **kwargs) -> list[HitDocument]:
        """Search for the top K documents in the collection for the query.
        Query-specific embedding is used if the model provides options for generating search query-optimized embeddings."""  # noqa: E501
        # Generate embedding for the query
        query_embedding = model.embed_for_search(query, **kwargs)
        # Search for the top K documents
        return self._search(collection, query_embedding, top_k)

    def search_image(
        self, model: MultimodalEmbeddingModel, collection: str, image_file: str, top_k: int = 5, **kwargs
    ) -> list[HitDocument]:
        """Search for the top K documents in the collection for the image."""
        # Generate embedding for the image
        query_embedding = model.embed_image(image_file, **kwargs)
        # Search for the top K documents
        return self._search(collection, query_embedding, top_k)

    @abstractmethod
    def _search(self, collection: str, query_embedding: list[float], top_k: int) -> list[HitDocument]:
        """Search for the top K documents."""
        pass

    @abstractmethod
    def list_collections(self) -> list[str]:
        """List all collections."""
        pass

    @abstractmethod
    def delete_collection(self, collection: str):
        """Delete a collection."""
        pass


class VectorStoreLocalFS(VectorStore):
    """Local file system vector store."""

    default_persist_path: str

    def __init__(self, persist_path: Optional[str] = None):
        super().__init__()
        if persist_path is None:
            persist_path = self.default_persist_path
        self.persist_path = persist_path

    def __str__(self):
        return f"{self.__class__.__name__}(vendor={self.vendor}, persist_path={self.persist_path})"


__vector_stores: dict[str, type[VectorStore]] = {}
__vector_store_factories: dict[str, Callable[[dict], VectorStore]] = {}


def register(vector_store_cls: type[VectorStore], factory: Callable[[dict], VectorStore]):
    """Register a vector store.
    Args:
        vector_store_cls (type[VectorStore]): The vector store class to register.
        factory (Callable[[dict], VectorStore]): A factory function to create instances of the vector store.
    """
    __vector_stores[vector_store_cls.vendor] = vector_store_cls
    __vector_store_factories[vector_store_cls.vendor] = factory


def available_vector_stores() -> list[type[VectorStore]]:
    """Get a list of available vector stores.
    Returns:
        list[type[VectorStore]]: A list of vector store classes.
    """
    return list(set(__vector_stores.values()))


def get_vector_store(vendor: str, args: dict) -> Optional[VectorStore]:
    """Get a vector store class by its vendor.
    Args:
        vendor (str): The vendor name.
        args (dict): Arguments to initialize the vector store.
    Returns:
        Optional[VectorStore]: The vector store class, or None if not found.
    """
    if vendor in __vector_store_factories:
        factory = __vector_store_factories[vendor]
        return factory(args)
    return None
