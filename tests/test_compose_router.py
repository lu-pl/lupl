"""Pytest entry point for lupl.ComposeRouter tests."""

from lupl import ComposeRouter
import pytest
from toolz import compose


def test_simple_compose_router():
    """Simple base test case for lupl.ComposeRouter.

    Check if the composed route generates the same result
    as the _components applied to the result of the method without routing.
    """
    _components = [lambda x: x + 1, lambda y: y * 2]

    class Foo:
        route = ComposeRouter(*_components)

        @route.register
        def method(self, x, y):
            return x * y

    foo = Foo()

    no_route = foo.method(2, 3)
    assert foo.route.method(2, 3) == compose(*_components)(no_route)


def test_simple_compse_router_unregistered_fail():
    _components = [lambda x: x + 1, lambda y: y * 2]

    class Foo:
        route = ComposeRouter(*_components)

        def method(self, x, y):
            return x * y

    foo = Foo()

    with pytest.raises(AttributeError):
        foo.route.method(2, 3)
