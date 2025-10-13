"""Pytest entry point for mutual constraint validation mixin."""

from typing import NamedTuple

import pytest

from pydantic import BaseModel, ConfigDict
from lupl import _MutualConstraintMixin
from lupl.pydantic_tools.mutual_constraint_validator import (
    MutualDependencyException,
    MutualExclusionException,
)


class Model(BaseModel, _MutualConstraintMixin):
    a: int | None = None
    b: int | None = None
    c: int | None = None
    d: int | None = None


class MutualConstraintParameter(NamedTuple):
    model: BaseModel
    model_config: ConfigDict
    model_init: dict
    exception: Exception | None = None


mutual_constraint_pass_parameters = [
    MutualConstraintParameter(
        model=Model,
        model_config=ConfigDict(),
        model_init={"a": 1, "c": 3},
        exception=None,
    ),
    MutualConstraintParameter(
        model=Model,
        model_config=ConfigDict(mutually_exclusive=[("a", "b")]),
        model_init={"a": 1, "c": 3},
        exception=None,
    ),
    MutualConstraintParameter(
        model=Model,
        model_config=ConfigDict(mutually_exclusive=[("a", "b")]),
        model_init={"b": 2, "c": 3, "d": 4},
        exception=None,
    ),
    MutualConstraintParameter(
        model=Model,
        model_config=ConfigDict(mutually_exclusive=[("a", "d")]),
        model_init={"a": 1, "b": 2, "c": 3},
        exception=None,
    ),
    MutualConstraintParameter(
        model=Model,
        model_config=ConfigDict(mutually_dependent=[("a", "b")]),
        model_init={"a": 1, "b": 2, "c": 3},
        exception=MutualDependencyException,
    ),
    MutualConstraintParameter(
        model=Model,
        model_config=ConfigDict(mutually_dependent=[("a", "b")]),
        model_init={"c": 3, "d": 4, "a": 1, "b": 2},
        exception=MutualDependencyException,
    ),
    MutualConstraintParameter(
        model=Model,
        model_config=ConfigDict(mutually_dependent=[("a", "d")]),
        model_init={"a": 1, "c": 3, "d": 4},
        exception=MutualDependencyException,
    ),
]

mutual_constraint_fail_parameters: list[MutualConstraintParameter] = [
    MutualConstraintParameter(
        model=Model,
        model_config=ConfigDict(mutually_exclusive=[("a", "b")]),
        model_init={"a": 1, "b": 2},
        exception=MutualExclusionException,
    ),
    MutualConstraintParameter(
        model=Model,
        model_config=ConfigDict(mutually_exclusive=[("a", "b")]),
        model_init={"a": 1, "b": 2, "c": 3, "d": 4},
        exception=MutualExclusionException,
    ),
    MutualConstraintParameter(
        model=Model,
        model_config=ConfigDict(mutually_exclusive=[("a", "d")]),
        model_init={"a": 1, "b": 2, "c": 3, "d": 4},
        exception=MutualExclusionException,
    ),
    MutualConstraintParameter(
        model=Model,
        model_config=ConfigDict(mutually_dependent=[("a", "b")]),
        model_init={"a": 1, "c": 3},
        exception=MutualDependencyException,
    ),
    MutualConstraintParameter(
        model=Model,
        model_config=ConfigDict(mutually_dependent=[("a", "b")]),
        model_init={"c": 3, "d": 4},
        exception=MutualDependencyException,
    ),
    MutualConstraintParameter(
        model=Model,
        model_config=ConfigDict(mutually_dependent=[("a", "d")]),
        model_init={"c": 3, "d": 4},
        exception=MutualDependencyException,
    ),
]


@pytest.mark.parametrize(
    MutualConstraintParameter._fields, mutual_constraint_pass_parameters
)
def test_happy_path_mutual_constrain_validator(
    model, model_config, model_init, exception
):
    model.model_config = model_config
    assert model(**model_init)


@pytest.mark.parametrize(
    MutualConstraintParameter._fields, mutual_constraint_fail_parameters
)
def test_sad_path_mutual_constrain_validator(
    model, model_config, model_init, exception
):
    model.model_config = model_config

    with pytest.raises(exception):
        model(**model_init)
