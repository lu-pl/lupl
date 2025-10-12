"""ComposeRouter: Utility for routing methods through a functional pipeline."""

from collections.abc import Callable

from toolz import compose


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

    def __init__(self, *components: Callable) -> None:
        self._components: tuple[Callable, ...] = components
        self._registry: list = []

    def register[F: Callable](self, f: F) -> F:
        self._registry.append(f.__name__)
        return f

    def __get__[T](self, instance: T, owner: type[T]):
        class _wrapper:
            def __init__(_self, other):
                _self.other = other

            def __getattr__(_self, name):
                if name in self._registry:
                    method = getattr(_self.other, name)
                    return compose(*self._components, method)

                raise AttributeError(f"Name '{name}' not registered.")

        return _wrapper(instance)
