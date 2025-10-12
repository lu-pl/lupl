"""Basic test for lupl.validate_model_field."""

import pytest

from pydantic import BaseModel
from lupl import validate_model_field


def test_validate_model_field_sad_path_missing_field():
    class Model(BaseModel):
        x: int

    with pytest.raises(ValueError):
        validate_model_field(model=Model, field="dne", value=None)


def test_validate_model_field_sad_path_invalid_value():
    class Model(BaseModel):
        x: int

    with pytest.raises(ValueError):
        validate_model_field(model=Model, field="x", value=1.1)
