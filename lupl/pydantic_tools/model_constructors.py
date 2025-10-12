"""Pydantic model constructors."""

from pydantic import BaseModel


def init_model_from_kwargs[ModelType: BaseModel](
    model: type[ModelType], **kwargs
) -> ModelType:
    """Instantiate a (potentially nested) model from (flat) kwargs.

    Example:

        class SimpleModel(BaseModel):
            x: int
            y: int


        class NestedModel(BaseModel):
            a: str
            b: SimpleModel


        class ComplexModel(BaseModel):
            p: str
            q: NestedModel


    model = instantiate_model_from_kwargs(ComplexModel, x=1, y=2, a="a value", p="p value")
    print(model)  # p='p value' q=NestedModel(a='a value', b=SimpleModel(x=1, y=2))
    """

    def _model_class_p(field_key, field_value, kwargs) -> bool:
        """Helper for _get_bindings.

        Check if a field is annoted with a model type and there is no applicable model instance kwarg.
        This triggers the recursive case in _get_bindings.
        """
        return isinstance(field_value.annotation, type(BaseModel)) and not isinstance(
            kwargs.get(field_key), BaseModel
        )

    def _construct_bindings(model: type[ModelType], **kwargs) -> dict:
        """Construct bindings needed for model instantiation from kwargs.

        If a field is annotated with a model type and there is no applicable model instance kwarg,
        trigger the recursive clause and consult kwargs for the nested model.
        """
        return {
            k: (
                v.annotation(**_construct_bindings(v.annotation, **kwargs))
                if _model_class_p(k, v, kwargs)
                else kwargs.get(k, v.default)
            )
            for k, v in model.model_fields.items()
        }

    return model(**_construct_bindings(model, **kwargs))
