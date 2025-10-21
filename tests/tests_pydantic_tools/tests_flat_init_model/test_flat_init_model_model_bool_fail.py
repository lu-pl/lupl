"""Pytest entry point for lupl.FlatInitModel model_bool failure tests."""

from lupl import ConfigDict, FlatInitModel
from pydantic import BaseModel
import pytest


class NestedModel1(BaseModel):
    model_config = ConfigDict(model_bool=["x"])


class NestedModel2(BaseModel):
    model_config = ConfigDict(model_bool=object())


class NestedModel3(BaseModel):
    model_config = ConfigDict(model_bool=None)


class Model1(BaseModel):
    nested: NestedModel1 | None = None


class Model2(BaseModel):
    nested: NestedModel2 | None = None


class Model3(BaseModel):
    nested: NestedModel3 | None = None


@pytest.mark.parametrize("model", [Model1, Model2, Model3])
def test_flat_init_model_model_bool_fail(model):
    constructor = FlatInitModel(model=model)

    with pytest.raises(ValueError):
        constructor()
