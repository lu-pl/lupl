"""A simple chunk iterator."""

from collections.abc import Iterator
from itertools import chain, islice
from typing import cast


def ichunk[T](iterator: Iterator[T], size: int) -> Iterator[Iterator[T]]:
    _missing = object()
    chunk = islice(iterator, size)

    if (first := next(chunk, _missing)) is _missing:
        return

    yield chain[T]([cast(T, first)], chunk)
    yield from ichunk(iterator, size=size)
