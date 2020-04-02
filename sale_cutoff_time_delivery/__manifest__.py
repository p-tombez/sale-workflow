# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)
{
    "name": "Sale Cutoff Time Delivery",
    "summary": "Schedule delivery orders according to cutoff preferences",
    "version": "13.0.1.0.0",
    "development_status": "Alpha",
    "category": "Warehouse Management",
    "website": "https://github.com/OCA/sale-workflow",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale_stock"],
    "data": ["views/res_partner.xml", "views/stock_warehouse.xml"],
}
