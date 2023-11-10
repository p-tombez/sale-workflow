# Copyright 2023 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Delivery State View",
    "summary": "Show the delivery state on sale order when not having sale_stock",
    "version": "16.0.1.0.0",
    "development_status": "Alpha",
    "category": "Uncategorized",
    "website": "https://github.com/OCA/sale-workflow",
    "author": " Akretion,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "sale_delivery_state",
    ],
    "excludes": ["sale_stock"],
    "data": [
        "views/sale_order_views.xml",
    ],
    "demo": [],
}
