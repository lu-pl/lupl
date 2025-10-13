"""Pytest entry point for lupl.CurryModel tests."""

from pydantic import BaseModel, Field
from lupl import CurryModel


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


def test_curry_default_arg_model_eager():
    class MyModel(BaseModel):
        x: int
        y: int
        z: int = 3

    curried = CurryModel(MyModel)
    x_curried = curried(x=1)
    assert isinstance(x_curried, CurryModel)

    model = x_curried(y=2)
    assert isinstance(model, BaseModel)


def test_curry_default_arg_model_non_eager():
    class MyModel(BaseModel):
        x: int
        y: int
        z: int = 3

    curried = CurryModel(MyModel, eager=False)
    x_curried = curried(x=1)
    assert isinstance(x_curried, CurryModel)

    y_curried = x_curried(y=2)
    assert isinstance(y_curried, CurryModel)

    model = y_curried(z=33)
    assert isinstance(model, BaseModel)
    assert model.z == 33
