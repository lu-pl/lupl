"""Pytest entry point for upto.CurryModel tests."""

from typing import TypedDict

from hypothesis import given
from pydantic import BaseModel, create_model
from upto import CurryModel


def test_simple_curry_model():
    class MyModel(BaseModel):
        x: str
        y: int
        z: tuple[str, int]

    curried_model1 = CurryModel(MyModel)
    curried_model1(x="1")
    curried_model1(y=2)
    model_instance1 = curried_model1(z=("3", 4))

    curried_model_2 = CurryModel(MyModel)
    model_instance_2 = curried_model_2(x="1")(y=2)(z=("3", 4))

    curried_model_3 = CurryModel(MyModel)
    model_instance_3 = curried_model_3(x="1", y=2)(z=("3", 4))

    assert model_instance1 == model_instance_2 == model_instance_3
