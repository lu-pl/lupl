"""Basic tests for lupl.ichunk."""

from collections.abc import Iterator
from typing import NamedTuple

from lupl import ichunk
import pytest


class IChunkTestParameter(NamedTuple):
    iterator: Iterator
    size: int
    expected: list[tuple]


params = [
    IChunkTestParameter(
        iterator=iter(range(5)), size=2, expected=[(0, 1), (2, 3), (4,)]
    ),
    IChunkTestParameter(
        iterator=iter(range(6)), size=2, expected=[(0, 1), (2, 3), (4, 5)]
    ),
    IChunkTestParameter(
        iterator=iter(range(6)),
        size=3,
        expected=[(0, 1, 2), (3, 4, 5)],
    ),
    IChunkTestParameter(iterator=iter(range(0)), size=2, expected=[]),
    IChunkTestParameter(iterator=iter(range(5)), size=5, expected=[(0, 1, 2, 3, 4)]),
    IChunkTestParameter(iterator=iter(range(5)), size=50, expected=[(0, 1, 2, 3, 4)]),
    IChunkTestParameter(iterator=iter(range(5)), size=0, expected=[]),
]


@pytest.mark.parametrize("param", params)
def test_ichunk(param):
    chunks = ichunk(iterator=param.iterator, size=param.size)
    result = [tuple(chunk) for chunk in chunks]

    assert result == param.expected
