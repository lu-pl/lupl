"""Model and kwargs data mappings for testing lupl.init_model_from_kwargs"""

from pydantic import BaseModel
from lupl.pydantic_tools.model_constructors import init_model_from_kwargs


class SimpleModel(BaseModel):
    x: int
    y: int = 3


class NestedModel(BaseModel):
    a: str
    b: SimpleModel


class ComplexModel(BaseModel):
    p: str
    q: NestedModel


init_model_from_kwargs_parameters = [
    (SimpleModel, [{"x": 1}, {"x": 1, "y": 2}]),
    (
        NestedModel,
        [
            {"x": 1, "a": "a value"},
            {"x": 1, "y": 2, "a": "a value"},
            {"a": "a value", "b": SimpleModel(x=1)},
            {"a": "a value", "b": SimpleModel(x=1, y=2)},
        ],
    ),
    (
        ComplexModel,
        [
            {"p": "p value", "a": "a value", "x": 1},
            {"p": "p value", "a": "a value", "x": 1, "y": 2},
            {
                "p": "p value",
                "q": init_model_from_kwargs(NestedModel, **{"a": "a value", "x": 1}),
            },
            {"p": "p value", "q": NestedModel(a="a value", b=SimpleModel(x=1))},
        ],
    ),
]
