# UPTo

![tests](https://github.com/lu-pl/upto/actions/workflows/tests.yml/badge.svg)
[![coverage](https://coveralls.io/repos/github/lu-pl/upto/badge.svg?branch=main&kill_cache=1)](https://coveralls.io/github/lu-pl/upto?branch=main&kill_cache=1)
[![PyPI version](https://badge.fury.io/py/upto.svg)](https://badge.fury.io/py/upto)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

UPTo - A personal collection of potentially generally Useful Python Tools.


## ComposeRouter
The ComposeRouter class allows to route attributes access for registered methods
through a functional pipeline constructed from components.
The pipeline is only triggered if a registered method is accessed via the ComposeRouter namespace.

```python
from upto import ComposeRouter

class Foo:
	route = ComposeRouter(lambda x: x + 1, lambda y: y * 2)

	@route.register
	def method(self, x, y):
		return x * y

	foo = Foo()

print(foo.method(2, 3))           # 6
print(foo.route.method(2, 3))     # 13
```

## Chunk Iterator

The `upto.ichunk` generator implements a simple chunk iterator that allows to lazily slice an Iterator into sub-iterators.

```python
from collections.abc import Iterator
from upto import ichunk

iterator: Iterator[int] = iter(range(10))
chunks: Iterator[Iterator[int]] = ichunk(iterator, size=3)

materialized = [tuple(chunk) for chunk in chunks]
print(materialized)  # [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)]
```

## Pydantic Tools

### CurryModel
The CurryModel constructor allows to sequentially initialize (curry) a Pydantic model.

```python
from upto import CurryModel

class MyModel(BaseModel):
	x: str
	y: int
	z: tuple[str, int]


curried_model = CurryModel(MyModel)

curried_model(x="1")
curried_model(y=2)

model_instance = curried_model(z=("3", 4))
print(model_instance)
```

CurryModel instances are recursive so it is also possible to do this:

```python
curried_model_2 = CurryModel(MyModel)
model_instance_2 = curried_model_2(x="1")(y=2)(z=("3", 4))
print(model_instance_2)
```

Currying turns a function of arity n into at most n functions of arity 1 and at least 1 function of arity n (and everything in between), so you can also do e.g. this:

```python
curried_model_3 = CurryModel(MyModel)
model_instance_3 = curried_model_3(x="1", y=2)(z=("3", 4))
print(model_instance_3)
```

### init_model_from_kwargs

The `init_model_from_kwargs` constructor allows to initialize (potentially nested) models from (flat) kwargs.

```python
class SimpleModel(BaseModel):
	x: int
	y: int = 3


class NestedModel(BaseModel):
	a: str
	b: SimpleModel


class ComplexModel(BaseModel):
	p: str
	q: NestedModel


# p='p value' q=NestedModel(a='a value', b=SimpleModel(x=1, y=2))
model_instance_1 = init_model_from_kwargs(
	ComplexModel, x=1, y=2, a="a value", p="p value"
)

# p='p value' q=NestedModel(a='a value', b=SimpleModel(x=1, y=3))
model_instance_2 = init_model_from_kwargs(
	ComplexModel, p="p value", q=NestedModel(a="a value", b=SimpleModel(x=1))
)

# p='p value' q=NestedModel(a='a value', b=SimpleModel(x=1, y=3))
model_instance_3 = init_model_from_kwargs(
	ComplexModel, p="p value", q=init_model_from_kwargs(NestedModel, a="a value", x=1)
)
```
