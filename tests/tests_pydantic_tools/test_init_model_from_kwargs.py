"""Pytest entry point for init_model_from_kwargs tests."""

import pytest

from tests.data.init_model_from_kwargs_parameters import (
    init_model_from_kwargs_parameters,
)
from lupl import init_model_from_kwargs


@pytest.mark.parametrize(("model", "kwargs"), init_model_from_kwargs_parameters)
def test_init_model_from_kwargs(model, kwargs):
    """Check if the init_model_from_kwargs constructor successfully inits a model based on kwargs."""
    for _kwargs in kwargs:
        model_instance = init_model_from_kwargs(model, **_kwargs)
        assert isinstance(model_instance, model)
