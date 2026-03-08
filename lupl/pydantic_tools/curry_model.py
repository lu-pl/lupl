"""CurryModel: Constructor for currying a Pydantic Model."""

from typing import Any, Self, overload

from pydantic import BaseModel, ValidationError


def validate_model_field(model: type[BaseModel], field: str, value: Any) -> Any:
    """Validate value for a single field given a model.

    Note: Using a TypeVar for value is not possible here,
    because Pydantic might coerce values (if not not in Strict Mode).
    """

    try:
        model(**{field: value})
    except ValidationError as e:
        for error in e.errors():
            if field in error["loc"]:
                raise ValidationError.from_exception_data(model.__name__, [error])

    return value


class CurryModel[TModel: BaseModel]:
    """Constructor for currying a Pydantic Model.

    A CurryModel instance can be called with kwargs which are run against
    the respective model field validators and kept in a kwargs cache.

    Calling a CurryModel object without passing kwargs triggers model instantiation;
    i.e. cached kwargs are passed to the model and the model instance is returned.
    """

    def __init__(self, model: type[TModel], fail_fast: bool = True) -> None:
        self.model = model
        self.fail_fast = fail_fast

        self._kwargs_cache: dict = {}

    def __repr__(self):  # pragma: no cover
        return f"CurryModel object {self._kwargs_cache}"

    @overload
    def __call__(self) -> TModel: ...  # pyright: ignore[reportOverlappingOverload]
    @overload
    def __call__(self, **kwargs) -> Self: ...

    def __call__(self, **kwargs: Any) -> Self | TModel:
        if self.fail_fast:
            for k, v in kwargs.items():
                validate_model_field(self.model, k, v)

        self._kwargs_cache.update(kwargs)

        if not kwargs:
            return self.model(**self._kwargs_cache)
        return self
