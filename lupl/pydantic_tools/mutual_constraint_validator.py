"""Mixin enabling Pydantic models to check for mutually dependent fields."""

from typing import NoReturn, Protocol

from pydantic import BaseModel, ConfigDict, model_validator


class MutualExclusionException(Exception):
    pass


class MutualDependencyException(Exception):
    pass


class _MutualConstraintTemplate(Protocol):
    constraint_id: str

    def condition(self, pair: tuple[str, str], model_data: dict) -> bool: ...

    def throw(self, pair: tuple[str, str]) -> NoReturn: ...


class MutualExclusionTemplate(_MutualConstraintTemplate):
    constraint_id = "mutually_exclusive"

    def condition(self, pair: tuple[str, str], model_data: dict) -> bool:
        return all(field in model_data for field in pair)

    def throw(self, pair: tuple[str, str]) -> NoReturn:
        raise MutualExclusionException(
            f"Fields {' and '.join(pair)} are mutually exclusive."
        )


class MutualDependencyTemplate(_MutualConstraintTemplate):
    constraint_id = "mutually_dependent"

    def condition(self, pair: tuple[str, str], model_data: dict) -> bool:
        return not all(field in model_data for field in pair)

    def throw(self, pair: tuple[str, str]) -> NoReturn:
        raise MutualDependencyException(
            f"Fields {' and '.join(pair)} are mutually dependent."
        )


class _MutualConstraintMixin:
    """Mixin for adding mutual exclusion and dependency validators to a model.

    Subclass _MutualConstrainMixin in a Pydantic model definition
    to add the validator to the model.

    The validator reads two keys from model_config:

    - mutually_exclusive: Iterable[tuple[str, str]]
    - mutually_dependent: Iterable[tuple[str, str]]

    and checks the model fields accordingly.
    """

    constraints = [
        MutualExclusionTemplate(),
        MutualDependencyTemplate(),
    ]

    @model_validator(mode="before")
    @classmethod
    def _check_mutual_constraints(cls, data: dict) -> dict:
        config = cls.model_config  # type: ignore

        for constraint in cls.constraints:
            if pairs := config.get(constraint.constraint_id):
                for pair in pairs:
                    if constraint.condition(pair, data):
                        constraint.throw(pair)

        return data
