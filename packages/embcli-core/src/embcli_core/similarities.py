from enum import Enum
from typing import Callable

import numpy as np


def dot_product(a: list[float], b: list[float]) -> float:
    """
    Compute the dot product between two vectors.
    """
    return float(np.dot(a, b))


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """
    Compute the cosine similarity between two vectors.
    """
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def euclidean_distance(a: list[float], b: list[float]) -> float:
    """
    Compute the Euclidean distance between two vectors.
    """
    return float(np.linalg.norm(np.array(a) - np.array(b)))


def manhattan_distance(a: list[float], b: list[float]) -> float:
    """
    Compute the Manhattan distance between two vectors.
    """
    return float(np.sum(np.abs(np.array(a) - np.array(b))))


class SimilarityFunction(Enum):
    DOT = "dot"
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    MANHATTAN = "manhattan"

    def get_similarity_function(self) -> Callable[[list[float], list[float]], float]:
        """
        Get the similarity function based on the enum value.
        """
        if self == SimilarityFunction.DOT:
            return dot_product
        elif self == SimilarityFunction.COSINE:
            return cosine_similarity
        elif self == SimilarityFunction.EUCLIDEAN:
            return euclidean_distance
        elif self == SimilarityFunction.MANHATTAN:
            return manhattan_distance
        else:
            raise ValueError(f"Unknown similarity function: {self}")
