from typing import get_args

from lupl import CurryModel
from lupl.pydantic_tools.flat_init.utils import (
    ModelBoolPredicate,
    _TModelBoolValue,
    _is_pydantic_model_static_type,
    _is_pydantic_model_union_static_type,
    get_model_bool_predicate,
)
from pydantic import BaseModel


class FlatInitModel[_TModel: BaseModel]:
    """Model constructor for initializing a potentially nested Pydantic model from flat kwargs.

    Nested model fields of a given model are recursively resolved;
    for model union fields, the first model type of the union is processed.
    """

    def __init__(self, model: type[_TModel], fail_fast: bool = True):
        self.model = model
        self.fail_fast = fail_fast

        self._curried_model = CurryModel(model=model, fail_fast=fail_fast)
        self._model_bool_value: _TModelBoolValue | None = self.model.model_config.get(
            "model_bool", None
        )

    def __call__(self, **kwargs) -> _TModel:
        """Run a FlatInitModel constructor to instantiate a Pydantic model from flat kwargs."""
        for field_name, field_info in self.model.model_fields.items():
            if _is_pydantic_model_static_type(field_info.annotation):
                nested_model = field_info.annotation
                field_value = FlatInitModel(
                    model=nested_model, fail_fast=self.fail_fast
                )(**kwargs)

            elif _is_pydantic_model_union_static_type(
                model_union := field_info.annotation
            ):
                nested_model_type: type[BaseModel] = next(
                    filter(_is_pydantic_model_static_type, get_args(model_union))
                )
                nested_model_instance = FlatInitModel(
                    model=nested_model_type, fail_fast=self.fail_fast
                )(**kwargs)
                model_bool_predicate: ModelBoolPredicate = get_model_bool_predicate(
                    model=nested_model_type
                )
                field_value = (
                    nested_model_instance
                    if model_bool_predicate(nested_model_instance)
                    else field_info.default
                )
            else:
                field_value = kwargs.get(field_name, field_info.default)

            self._curried_model(**{field_name: field_value})

        model_instance = self._curried_model()

        assert isinstance(model_instance, self.model)
        return model_instance
