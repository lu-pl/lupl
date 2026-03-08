"""Pytest entry point for lupl.CurryModel tests."""

from pydantic import BaseModel, ConfigDict, Field

from lupl import CurryModel


def test_simple_curry_model():
    class MyModel(BaseModel):
        x: str
        y: int
        z: tuple[str, int]

    curried_model1 = CurryModel(MyModel)
    curried_model1(x="1")
    curried_model1(y=2)
    model_instance1 = curried_model1(z=("3", 4))()

    curried_model_2 = CurryModel(MyModel)
    model_instance_2 = curried_model_2(x="1")(y=2)(z=("3", 4))()

    curried_model_3 = CurryModel(MyModel)
    model_instance_3 = curried_model_3(x="1", y=2)(z=("3", 4))()

    assert model_instance1 == model_instance_2 == model_instance_3


def test_curry_model_aliasing():
    class Model(BaseModel):
        model_config = ConfigDict(
            alias_generator=lambda field_name: field_name * 3, validate_by_name=True
        )

        a: int
        b: int = Field(validation_alias="B")
        c: int = Field(validation_alias="C", alias_priority=1)
        d: int = Field(validation_alias="D", alias_priority=2)

    curry_model = CurryModel(model=Model)(aaa=1)(B=2)(ccc=3)(D=4)(e=5)(f=6)(g=7)(h=8)
    curry_model()

    curry_model = CurryModel(model=Model)(a=1)(b=2)(c=3)(d=4)(e=5)(f=6)(g=7)(h=8)
    curry_model()
