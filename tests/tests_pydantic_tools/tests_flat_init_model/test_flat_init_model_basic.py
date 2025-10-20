"""Pytest entry point for for basic lupl.FlatInitModel test."""

from typing import Any, NamedTuple

from lupl import ConfigDict, FlatInitModel
from pydantic import BaseModel
import pytest


class FlatInitTestParameter(NamedTuple):
    model: type[BaseModel]
    kwargs: dict[str, Any]
    expected: dict[str, Any]


class DeeplyNestedModel1(BaseModel):
    z: int


class NestedModel1(BaseModel):
    y: int
    deeply_nested: DeeplyNestedModel1


class NestedModel2(NestedModel1):
    model_config = ConfigDict(model_bool="y")


class NestedModel3(NestedModel1):
    model_config = ConfigDict(model_bool=lambda model: model.y < 0)


class NestedModel4(NestedModel1):
    model_config = ConfigDict(model_bool={"y", "y2"})

    y2: int = 0


class Model1(BaseModel):
    x: int
    nested: NestedModel1


class Model2(Model1):
    model_config = ConfigDict(extra="forbid")


class Model3(Model1):
    x: int = 42


class Model4(BaseModel):
    x: int
    nested: NestedModel2 | str = "default"


class Model5(BaseModel):
    x: int
    nested: NestedModel3 | str = "default"


class Model6(BaseModel):
    x: int
    nested: NestedModel4 | str = "default"


class Model7(BaseModel):
    x: int
    nested: NestedModel1 | None = None


class Model8(BaseModel):
    x: int
    nested: DeeplyNestedModel1 | None = None


params: list[FlatInitTestParameter] = [
    FlatInitTestParameter(
        model=Model1,
        kwargs={"x": 1, "y": 2, "z": 3},
        expected={"x": 1, "nested": {"y": 2, "deeply_nested": {"z": 3}}},
    ),
    FlatInitTestParameter(
        model=Model2,
        kwargs={"x": 1, "y": 2, "z": 3},
        expected={"x": 1, "nested": {"y": 2, "deeply_nested": {"z": 3}}},
    ),
    FlatInitTestParameter(
        model=Model1,
        kwargs={"x": 1.0, "y": 2.0, "z": 3.0},
        expected={"x": 1, "nested": {"y": 2, "deeply_nested": {"z": 3}}},
    ),
    FlatInitTestParameter(
        model=Model3,
        kwargs={"x": 1, "y": 2, "z": 3},
        expected={"x": 1, "nested": {"y": 2, "deeply_nested": {"z": 3}}},
    ),
    FlatInitTestParameter(
        model=Model3,
        kwargs={"y": 2, "z": 3},
        expected={"x": 42, "nested": {"y": 2, "deeply_nested": {"z": 3}}},
    ),
    FlatInitTestParameter(
        model=Model4,
        kwargs={"x": 1, "y": 2, "z": 3},
        expected={"x": 1, "nested": {"y": 2, "deeply_nested": {"z": 3}}},
    ),
    FlatInitTestParameter(
        model=Model4,
        kwargs={"x": 1, "y": 0, "z": 3},
        expected={"x": 1, "nested": "default"},
    ),
    FlatInitTestParameter(
        model=Model5,
        kwargs={"x": 1, "y": 0, "z": 3},
        expected={"x": 1, "nested": "default"},
    ),
    FlatInitTestParameter(
        model=Model5,
        kwargs={"x": 1, "y": -2, "z": 3},
        expected={"x": 1, "nested": {"y": -2, "deeply_nested": {"z": 3}}},
    ),
    FlatInitTestParameter(
        model=Model6,
        kwargs={"x": 1, "y": 2, "z": 3},
        expected={"x": 1, "nested": "default"},
    ),
    FlatInitTestParameter(
        model=Model7,
        kwargs={"x": 1, "y": 2, "z": 3},
        expected={"x": 1, "nested": {"y": 2, "deeply_nested": {"z": 3}}},
    ),
    FlatInitTestParameter(
        model=Model8,
        kwargs={"x": 1, "z": 3},
        expected={"x": 1, "nested": {"z": 3}},
    ),
    FlatInitTestParameter(
        model=Model8,
        kwargs={"x": 1, "z": 0},
        expected={"x": 1, "nested": None},
    ),
]


@pytest.mark.parametrize("param", params)
def test_basic_flat_init_model(param):
    constructor = FlatInitModel(model=param.model)
    instance = constructor(**param.kwargs)

    assert instance.model_dump() == param.expected
