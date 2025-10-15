"""Basic tests for lupl.ComposeRouter"""

from typing import Any, NamedTuple

from lupl import ComposeRouter
import pytest


class ComposeRouterTestParameter(NamedTuple):
    instance: object
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    expected: Any
    expected_route: Any
    expected_route_left: Any


class TestClass1:
    route = ComposeRouter(lambda x: x + 1, lambda y: y * 2)

    @route.register
    def method(self, x, y):
        return x * y


class TestClass2:
    route = ComposeRouter(lambda x: x + 1, lambda y: y * 2, left_associative=True)

    @route.register
    def method(self, x, y):
        return x * y


class TestClass3:
    route = ComposeRouter(str, lambda x: f"{x}1", int, lambda x: f"{x}1", str)

    @route.register
    def method(self):
        return 1


class TestClass4:
    route = ComposeRouter(int, lambda x: f"{x}1")

    @route.register
    def method(self):
        return 1


class TestClass5:
    route = ComposeRouter(int, lambda x: f"{x}1")

    @route.register
    def method(self):
        return 1

    @route.register
    def method2(self):
        return 2


params = [
    ComposeRouterTestParameter(
        instance=TestClass1(),
        args=(2, 3),
        kwargs={},
        expected=6,
        expected_route=13,
        expected_route_left=14,
    ),
    ComposeRouterTestParameter(
        instance=TestClass2(),
        args=(2, 3),
        kwargs={},
        expected=6,
        expected_route=14,
        expected_route_left=14,
    ),
    ComposeRouterTestParameter(
        instance=TestClass3(),
        args=(),
        kwargs={},
        expected=1,
        expected_route="111",
        expected_route_left="111",
    ),
    ComposeRouterTestParameter(
        instance=TestClass4(),
        args=(),
        kwargs={},
        expected=1,
        expected_route=11,
        expected_route_left="11",
    ),
    ComposeRouterTestParameter(
        instance=TestClass5(),
        args=(),
        kwargs={},
        expected=1,
        expected_route=11,
        expected_route_left="11",
    ),
]


@pytest.mark.parametrize("param", params)
def test_basic_compose_router(param):
    args, kwargs = param.args, param.kwargs

    assert param.instance.method(*args, **kwargs) == param.expected
    assert param.instance.route.method(*args, **kwargs) == param.expected_route
    assert (
        param.instance.route(left_associative=True).method(*args, **kwargs)
        == param.expected_route_left
    )
    # repeat to check that left_associative is not altered
    assert param.instance.method(*args, **kwargs) == param.expected
