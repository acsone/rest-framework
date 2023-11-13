from dataclasses import dataclass
from typing import Annotated, Any, Generic, TypeVar

from extendable_pydantic import StrictExtendableBaseModel
from pydantic_core import SchemaValidator, core_schema

from odoo.addons.fastapi.context import odoo_env_ctx

from pydantic import Field, GetCoreSchemaHandler

T = TypeVar("T")


class PagedCollection(StrictExtendableBaseModel, Generic[T]):
    """A paged collection of items"""

    # This is a generic model. The type of the items is defined by the generic type T.
    # It provides you a common way to return a paged collection of items of
    # extendable models. It's based on the StrictExtendableBaseModel to ensure
    # a strict validation when used within the odoo fastapi framework.

    count: Annotated[int, Field(..., description="The count of items into the system")]
    items: list[T]


@dataclass
class OdooSelectionField:
    """A pydantic field info to specify a selection field from odoo

    This field info applies only to string fields. It will be used to
    generate a literal schema with the possible values from the odoo field.

    Example:

        class MyModel(StrictExtendableBaseModel):
            my_field: Annotated[str, OdooSelectionField(model='my.model', field='my_field')]

    """

    model: str
    field: str

    def _get_selection(self) -> list[str]:
        """
        Get the list of possible values from the odoo field specified
        in the pydantic field info.
        """
        try:
            env = odoo_env_ctx.get()
            odoo_field = env[self.model]._fields(self.field)
            return odoo_field.get_values(env)
        except LookupError:
            return [""]

    def __get_pydantic_core_schema__(
        self, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        if not self.model or not self.field:
            raise ValueError("model and field must be set")
        schema = handler(source)  # get the CoreSchema from the type / inner constraints
        if schema["type"] != "str":
            raise TypeError("OdooSelectionField can only be applied to strings")
        literal_schema = handler(core_schema.literal_schema(self._get_selection()))
        # json_schema.update_json_schema(literal_schema, {"description":'This is a description'})
        validator = SchemaValidator(schema)
        return core_schema.no_info_after_validator_function(
            lambda v, schema_validator=validator: schema_validator.validate_python(v),
            literal_schema,
        )
