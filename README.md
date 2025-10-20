# lupl 👾😺

![tests](https://github.com/lu-pl/lupl/actions/workflows/tests.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/lu-pl/lupl/badge.svg?branch=lupl/rename)](https://coveralls.io/github/lu-pl/lupl?branch=lupl/rename)
[![PyPI version](https://badge.fury.io/py/lupl.svg)](https://badge.fury.io/py/lupl)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

A collection of potentially generally useful Python utilities.

## Installation

`lupl` is a [PEP-621](https://peps.python.org/pep-0621/)-compliant package and available on [PyPI](https://pypi.org/project/lupl/).

## Usage

### ComposeRouter

The `ComposeRouter` class allows to route attributes access for registered methods
through a functional pipeline constructed from components.
The pipeline is only triggered if a registered method is accessed via the `ComposeRouter` namespace.

```python
from lupl import ComposeRouter

class Foo:
	route = ComposeRouter(lambda x: x + 1, lambda y: y * 2)

	@route.register
	def method(self, x, y):
		return x * y

	foo = Foo()

print(foo.method(2, 3))           # 6
print(foo.route.method(2, 3))     # 13
```

By default, composition in `ComposeRouter` is *right-associative*.

Associativity can be controlled by setting the `left_associative: bool` kwarg either when creating the `ComposeRouter` instance or when calling it.


```python
class Bar:
	route = ComposeRouter(lambda x: x + 1, lambda y: y * 2, left_associative=True)

	@route.register
	def method(self, x, y):
		return x * y

bar = Bar()

print(bar.method(2, 3))  # 6
print(bar.route.method(2, 3))  # 14
print(bar.route(left_associative=False).method(2, 3))  # 13
```

### Chunk Iterator

The `ichunk` generator implements a simple chunk iterator that allows to lazily slice an Iterator into sub-iterators.

```python
from collections.abc import Iterator
from lupl import ichunk

iterator: Iterator[int] = iter(range(10))
chunks: Iterator[Iterator[int]] = ichunk(iterator, size=3)

materialized = [tuple(chunk) for chunk in chunks]
print(materialized)  # [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)]
```

### Pydantic Tools

#### CurryModel

The `CurryModel` constructor allows to sequentially initialize (curry) a Pydantic model.

```python
from lupl import CurryModel

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

`CurryModel` instances are recursive so it is also possible to do this:

```python
curried_model_2 = CurryModel(MyModel)
model_instance_2 = curried_model_2(x="1")(y=2)(z=("3", 4))
print(model_instance_2)
```

Currying turns a function of arity *n* into at most *n* functions of arity 1 and at least 1 function of arity *n* (and everything in between), so you can also do e.g. this:

```python
curried_model_3 = CurryModel(MyModel)
model_instance_3 = curried_model_3(x="1", y=2)(z=("3", 4))
print(model_instance_3)
```

#### FlatInitModel

The `FlatInitModel` constructor allows to instantiate a potentially deeply nested Pydantic model from flat kwargs.

```python
from lupl import FlatInitModel
from pydantic import BaseModel

class DeeplyNestedModel(BaseModel):
	z: int

class NestedModel(BaseModel):
	y: int
	deeply_nested: DeeplyNestedModel

class Model(BaseModel):
	x: int
	nested: NestedModel

constructor = FlatInitModel(model=Model)

instance: Model = constructor(x=1, y=2, z=3)
instance.model_dump()  # {'x': 1, 'nested': {'y': 2, 'deeply_nested': {'z': 3}}}
```


`FlatInitModel` also handles model union types by processing the first model type of the union.

A common use case for model union types is e.g. to assign a default value to a model union typed field in case a nested model instance does not meet certain criteria, i.e. fails a predicate.

The `model_bool` parameter in `lupl.ConfigDict` allows to specify the condition for *model truthiness* - if the existential condition of a model is met, the model instance gets assigned to the model field, else the constructor falls back to the default value.


The default condition for model truthiness is that *any* model field must be truthy for the model to be considered truthy.

The `model_bool` parameter takes either

- a callable object of arity 1 that receives the model instance at runtime,
- a `str` denoting a field of the model that must be truthy in order for the model to be truthy
- a `set[str]` denoting fields of the model, all of which must be truthy for the model to be truthy.


The following example defines the truth condition for `DeeplyNestedModel` to be `gt3`. `NestedModel` defines a model union type with a default value - if the `model_bool` predicate fails, the constructor falls back to the default:

```python
from lupl import ConfigDict, FlatInitModel
from pydantic import BaseModel

class DeeplyNestedModel(BaseModel):
	model_config = ConfigDict(model_bool=lambda model: model.z > 3)

	z: int

class NestedModel(BaseModel):
	y: int
	deeply_nested: DeeplyNestedModel | str = "default"

class Model(BaseModel):
	x: int
	nested: NestedModel

constructor = FlatInitModel(model=Model)

instance: Model = constructor(x=1, y=2, z=3)
instance.model_dump()  # {'x': 1, 'nested': {'y': 2, 'deeply_nested': 'default'}}
```

If the existential condition of the model is met, the model instance gets assigned:

```python
instance: Model = constructor(x=1, y=2, z=4)
instance.model_dump()  # {'x': 1, 'nested': {'y': 2, 'deeply_nested': {'z': 4}}}
```
