"""CurryModel: Constructor for currying a Pydantic Model."""

from typing import Any, Self

from pydantic import BaseModel, ValidationError


def validate_model_field(model: type[BaseModel], field: str, value: Any) -> Any:
    """Validate value for a single field given a model.

    Note: Using a TypeVar for value is not possible here,
    because Pydantic might coerce values (if not not in Strict Mode).
    """

    if field not in model.model_fields:
        raise ValueError(f"'{field}' does not denote a field of model '{model}'.")

    try:
        model(**{field: value})
    except ValidationError as e:
        for error in e.errors():
            if field in error["loc"]:
                raise ValidationError.from_exception_data(model.__name__, [error])

    return value


class CurryModel[_TModelInstance: BaseModel]:
    """Constructor for currying a Pydantic Model.

    A CurryModel instance can be called with kwargs which are run against
    the respective model field validators and kept in a kwargs cache.
    Once the model can be instantiated, calling a CurryModel object will
    instantiate the Pydantic model and return the model instance.

    If the eager flag is True (default), model field default values are
    added to the cache automatically, which means that models can be instantiated
    as soon possible, i.e. as soon as all /required/ field values are provided.

    If the fail_fast flag is True (default), the constructor raises a ValueError
    as soon as a value fails to validate against a field constraint.
    """

    def __init__(
        self, model: type[_TModelInstance], eager: bool = True, fail_fast: bool = True
    ) -> None:
        self.model = model
        self.eager = eager
        self.fail_fast = fail_fast

        self._kwargs_cache: dict = (
            {k: v.default for k, v in model.model_fields.items() if not v.is_required()}
            if eager
            else {}
        )

    def __repr__(self):  # pragma: no cover
        return f"CurryModel object {self._kwargs_cache}"

    def __call__(self, **kwargs: Any) -> Self | _TModelInstance:
        if self.fail_fast:
            for k, v in kwargs.items():
                validate_model_field(self.model, k, v)

        self._kwargs_cache.update(kwargs)

        if self.model.model_fields.keys() == self._kwargs_cache.keys():
            return self.model(**self._kwargs_cache)
        return self
