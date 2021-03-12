# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductPricelist(models.Model):

    _inherit = "product.pricelist"

    def get_products_price(
        self, products, quantities, partners, date=False, uom_id=False
    ):
        new_date = date
        force_pricelist_date = self.env.context.get("force_pricelist_date")
        if force_pricelist_date:
            new_date = force_pricelist_date
        return super().get_products_price(
            products, quantities, partners, new_date, uom_id
        )
