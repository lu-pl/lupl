"""Basic sad path tests for lupl.ComposeRouter."""

from lupl import ComposeRouter
import pytest


class TestClassFailure1:
    route = ComposeRouter(lambda x: x + 1, lambda y: y * 2)

    def method(self, x, y):
        return x * y


def test_compose_router_attribute_failure():
    instance = TestClassFailure1()

    with pytest.raises(AttributeError):
        instance.route.method(2, 3)
