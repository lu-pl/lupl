# UPTo

[![PyPI version](https://badge.fury.io/py/upto.svg)](https://badge.fury.io/py/upto)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![image](https://img.shields.io/pypi/v/ruff.svg)](https://pypi.python.org/pypi/ruff)

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

## CurryModel
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
