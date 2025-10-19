"""Utils for the lupl.FlatInitModel constructor."""

from types import UnionType
from typing import (
    Any,
    Protocol,
    TypeAlias,
    TypeGuard,
    Union,
    cast,
    get_args,
    get_origin,
    runtime_checkable,
)

from pydantic import BaseModel, ConfigDict as PydanticConfigDict


@runtime_checkable
class ModelBoolPredicate[_TModel: BaseModel](Protocol):
    """Type for model_bool predicate functions."""

    def __call__(self, model: _TModel) -> bool: ...


_TModelBoolValue: TypeAlias = ModelBoolPredicate | str | set[str]


class ConfigDict(PydanticConfigDict, total=False):
    model_bool: _TModelBoolValue


def default_model_bool_predicate(model: BaseModel) -> bool:
    """Default predicate for determining model truthiness.

    Adheres to ModelBoolPredicate.
    """
    return any(dict(model).values())


def _get_model_bool_predicate_from_config_value(
    model_bool_value: _TModelBoolValue,
) -> ModelBoolPredicate:
    """Get a model_bool predicate function given the value of the model_bool config setting."""
    match model_bool_value:
        case ModelBoolPredicate():
            return model_bool_value
        case str():
            return lambda model: bool(dict(model)[model_bool_value])
        case set():
            return lambda model: all(map(lambda k: dict(model)[k], model_bool_value))
        case _:
            msg = (
                f"Expected type {_TModelBoolValue} for model_bool config setting. "
                f"Got '{model_bool_value}'."
            )
            raise ValueError(msg)


def get_model_bool_predicate(model: type[BaseModel] | BaseModel) -> ModelBoolPredicate:
    """Get the applicable model_bool predicate function given a model."""
    _missing = object()
    if (model_bool_value := model.model_config.get("model_bool", _missing)) is _missing:
        model_bool_predicate = default_model_bool_predicate
    else:
        model_bool_predicate = _get_model_bool_predicate_from_config_value(
            # cast and see what happens at runtime...
            cast(_TModelBoolValue, model_bool_value)
        )

    return model_bool_predicate


def _is_pydantic_model_static_type(obj: Any) -> TypeGuard[type[BaseModel]]:
    """Check if object is a Pydantic model type."""
    return (
        isinstance(obj, type) and issubclass(obj, BaseModel) and (obj is not BaseModel)
    )


def _is_pydantic_model_union_static_type(
    obj: Any,
) -> TypeGuard[UnionType]:
    """Check if object is a union type of a Pydantic model."""
    is_union_type: bool = get_origin(obj) in (UnionType, Union)
    has_any_model: bool = any(
        _is_pydantic_model_static_type(obj) for obj in get_args(obj)
    )

    return is_union_type and has_any_model
