# Copyright 2020 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class ComponentBuilder(models.AbstractModel):
    _inherit = "component.builder"

    @api.model_cr
    def _register_hook(self):
        super()._register_hook()
        # The order for calling the "_register_hook" on model is random
        # Indeed the Environment is a collections.abc.Mapping
        # that is not ordered and so the order is random
        # The build of the registry service must be done after the build
        # of "component.builder" so we call manually here the build after
        # calling super
        self.env["rest.service.registration"]._register_registry()
