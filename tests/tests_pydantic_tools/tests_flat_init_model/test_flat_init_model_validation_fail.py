"""Pytest entry point for lupl.FlatInitBase fail tests."""

from typing import Any, NamedTuple

from lupl import FlatInitModel
from pydantic import BaseModel, ValidationError
import pytest


class FlatInitFailParameter(NamedTuple):
    model: type[BaseModel]
    kwargs: dict[str, Any]
    errors: list[dict[str, Any]]
    fail_fast: bool = True


class DeeplyNestedModel(BaseModel):
    z: int


class NestedModel(BaseModel):
    y: int
    deeply_nested: DeeplyNestedModel


class Model(BaseModel):
    x: int
    nested: NestedModel


class SimpleModel(BaseModel):
    x: int
    y: int


params = [
    FlatInitFailParameter(
        model=Model,
        kwargs={"x": 1, "y": 2.1, "z": 3},
        errors=[
            {
                "type": "int_from_float",
                "loc": ("y",),
                "msg": "Input should be a valid integer, got a number with a fractional part",
                "input": 2.1,
                "url": "https://errors.pydantic.dev/2.12/v/int_from_float",
            }
        ],
    ),
    FlatInitFailParameter(
        model=Model,
        kwargs={"x": 1, "y": 2, "z": 3.1},
        errors=[
            {
                "type": "int_from_float",
                "loc": ("z",),
                "msg": "Input should be a valid integer, got a number with a fractional part",
                "input": 3.1,
                "url": "https://errors.pydantic.dev/2.12/v/int_from_float",
            }
        ],
    ),
    FlatInitFailParameter(
        model=Model,
        kwargs={"x": 1, "y": 2.1, "z": 3.1},
        errors=[
            {
                "type": "int_from_float",
                "loc": ("y",),
                "msg": "Input should be a valid integer, got a number with a fractional part",
                "input": 2.1,
                "url": "https://errors.pydantic.dev/2.12/v/int_from_float",
            }
        ],
        fail_fast=True,
    ),
    FlatInitFailParameter(
        model=Model,
        kwargs={"x": 1, "y": 2.1, "z": 3.1},
        errors=[
            {
                "type": "int_from_float",
                "loc": ("z",),
                "msg": "Input should be a valid integer, got a number with a fractional part",
                "input": 3.1,
                "url": "https://errors.pydantic.dev/2.12/v/int_from_float",
            }
        ],
        fail_fast=False,
    ),
    FlatInitFailParameter(
        model=SimpleModel,
        kwargs={"x": 1.1, "y": 2.1},
        errors=[
            {
                "type": "int_from_float",
                "loc": ("x",),
                "msg": "Input should be a valid integer, got a number with a fractional part",
                "input": 1.1,
                "url": "https://errors.pydantic.dev/2.12/v/int_from_float",
            },
            {
                "type": "int_from_float",
                "loc": ("y",),
                "msg": "Input should be a valid integer, got a number with a fractional part",
                "input": 2.1,
                "url": "https://errors.pydantic.dev/2.12/v/int_from_float",
            },
        ],
        fail_fast=False,
    ),
    FlatInitFailParameter(
        model=SimpleModel,
        kwargs={"x": 1.1, "y": 2.1},
        errors=[
            {
                "type": "int_from_float",
                "loc": ("x",),
                "msg": "Input should be a valid integer, got a number with a fractional part",
                "input": 1.1,
                "url": "https://errors.pydantic.dev/2.12/v/int_from_float",
            }
        ],
        fail_fast=True,
    ),
]


@pytest.mark.parametrize("param", params)
def test_flat_init_model_validation_fail(param):
    constructor = FlatInitModel(model=param.model, fail_fast=param.fail_fast)

    with pytest.raises(ValidationError) as excinfo:
        constructor(**param.kwargs)

    errors = excinfo.value.errors()
    assert param.errors == errors
