# Copyright 2023 ACSONE SA/NV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from typing import Annotated

from extendable_pydantic import ExtendableBaseModel

from ..schemas import OdooSelectionField
from .common import FastAPITransactionCase


class TestSelectionField(FastAPITransactionCase):
    class PartnerType(ExtendableBaseModel):
        partner_type: Annotated[
            str, OdooSelectionField(model="res.partner", field="type")
        ]

    def test_selection_field(self):
        schema = self.PartnerType.model_json_schema()
        selection_values = self.env["res.partner"]._fields["type"].get_values(self.env)
        self.assertEqual(schema["properties"]["partner_type"]["enum"], selection_values)
