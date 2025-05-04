import pytest
from embcli_core.similarities import (
    SimilarityFunction,
    cosine_similarity,
    dot_product,
    euclidean_distance,
    manhattan_distance,
)


def test_similarity_function_dot():
    fn = SimilarityFunction.DOT.get_similarity_function()
    assert fn == dot_product
    assert fn([1, 2], [3, 4]) == 11.0

    fn = SimilarityFunction.COSINE.get_similarity_function()
    assert fn == cosine_similarity
    assert fn([1, 2], [3, 4]) == pytest.approx(0.983, 0.001)

    fn = SimilarityFunction.EUCLIDEAN.get_similarity_function()
    assert fn == euclidean_distance
    assert fn([1, 2], [3, 4]) == pytest.approx(2.828, 0.001)

    fn = SimilarityFunction.MANHATTAN.get_similarity_function()
    assert fn == manhattan_distance
    assert fn([1, 2], [3, 4]) == 4.0
