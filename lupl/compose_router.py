"""ComposeRouter: Utility for routing methods through a functional pipeline."""

from collections.abc import Callable
from typing import Self

from toolz import compose, compose_left


class ComposeRouter:
    """ComposeRouter.

    This class routes attributes access for registered methods
    through a functional pipeline constructed from components.

    Example:

    class Foo:
        route = ComposeRouter(lambda x: x + 1, lambda y: y * 2)

        @route.register
        def method(self, x, y):
            return x * y

    foo = Foo()

    print(foo.method(2, 3))           # 6
    print(foo.route.method(2, 3))     # 13
    """

    def __init__(self, *components: Callable, left_associative: bool = False) -> None:
        self.components: tuple[Callable, ...] = components
        self.left_associative = left_associative

        self._registry: list[str] = []

    def register[F: Callable](self, f: F) -> F:
        """Register a method for routing through the component pipeline."""

        self._registry.append(f.__name__)
        return f

    def __get__[Self](self, instance: Self, owner: type[Self]):
        class _BoundRouter:
            """_BoundRouter is a heavily closured wrapper for handling compose calls.

            Upon attribute access on the ComposeRouter descriptor,
            _BoundRouter acts as an intermediary dispatcher that returns a composed callable
            that applies the specified pipeline components to the requested method.

            """

            def __init__(_self):
                _self.left_associative = self.left_associative

            def __call__(_self, *, left_associative: bool):
                _self.left_associative = left_associative
                return _self

            def __getattr__(_self, name):
                if name in self._registry:
                    method = getattr(instance, name)

                    if _self.left_associative:
                        return compose_left(method, *self.components)
                    return compose(*self.components, method)

                raise AttributeError(f"Name '{name}' not registered.")

        return _BoundRouter()
