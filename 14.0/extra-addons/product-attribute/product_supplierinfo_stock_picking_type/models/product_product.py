# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _prepare_sellers(self, params=False):
        res = super()._prepare_sellers(params)
        if params and params.get("order_id"):
            return res.filtered(
                lambda x: not x.picking_type_id
                or x.picking_type_id == params.get("order_id").picking_type_id
            )
        return res
