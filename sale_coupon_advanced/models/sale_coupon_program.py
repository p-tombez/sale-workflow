# Copyright 2020 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, exceptions, fields, models


class SaleCouponProgram(models.Model):
    _inherit = "sale.coupon.program"

    is_cumulative = fields.Boolean(string="None-cumulative Promotion")
    reward_pricelist_id = fields.Many2one("product.pricelist", string="Pricelist")
    # Add possibility to use discount only on first order of a customer
    first_order_only = fields.Boolean(
        string="Apply only first",
        help="Apply only on the first order of each client matching the conditions",
    )

    first_n_customer_orders = fields.Integer(
        help="Maximum number of sales orders of the customer in which reward \
         can be provided",
        string="Apply only on the next ",
        default=0,
    )
    is_reward_product_forced = fields.Boolean(
        string="Unordered product",
        default=False,
        help="If checked, the reward product will be added if not ordered.",
    )

    def _check_promo_code(self, order, coupon_code):

        order_count = self._get_order_count(order)
        if self.first_order_only and order_count:
            return {"error": _("Coupon can be used only for the first sale order!")}
        max_order_number = self.first_n_customer_orders
        if max_order_number and order_count >= max_order_number:
            return {
                "error": _(
                    "Coupon can be used only for the first {} sale order!"
                ).format(max_order_number)
            }

        # Do not return product unordered error message if
        # `is_reward_product_forced` is selected
        message = _(
            "The reward products should be in the sales order lines to"
            " apply the discount."
        )
        res = super()._check_promo_code(order, coupon_code)
        if res.get("error") == message and self.is_reward_product_forced:
            return {}
        return res

    @api.model
    def _filter_programs_from_common_rules(self, order, next_order=False):
        # Return the programs when `is_reward_product_forced` is selected
        # and reward product not already ordered

        initial_programs = self.browse(self.ids)
        # TODO there is inconsistency in order of programs which program
        # should run first?

        for program in initial_programs:
            if (
                program.reward_type == "product"
                and program.is_reward_product_forced
                and not order._is_reward_in_order_lines(program)
            ):
                order.add_reward_line_values(program)

        programs = super()._filter_programs_from_common_rules(order, next_order)
        programs = programs._filter_first_order_programs(order)
        programs = programs._filter_n_first_order_programs(order)

        return programs

    @api.constrains("first_n_customer_orders")
    def _constrains_first_n_orders_positive(self):
        for record in self:
            if record.first_n_customer_orders < 0:
                raise exceptions.ValidationError(
                    _("`Apply only on the next` should not be a negative value.")
                )

    def _get_order_count(self, order):
        return self.env["sale.order"].search_count(
            [
                ("partner_id", "=", order.partner_id.id),
                ("state", "!=", "cancel"),
                ("id", "!=", order.id),
            ]
        )

    def _filter_first_order_programs(self, order):
        """
        Filter programs where first_order_only is True,
        and the customer have already ordered before.
        """
        if self._get_order_count(order):
            return self.filtered(lambda program: not program.first_order_only)
        return self

    def _filter_n_first_order_programs(self, order):
        """
        Filter programs where first_n_customer_orders is set, and
        the max number of orders have already been reached by the customer.
        """
        order_count = self._get_order_count(order)
        filtered_programs = self.env[self._name]
        for program in self:
            if (
                program.first_n_customer_orders
                and order_count >= program.first_n_customer_orders
            ):
                continue
            filtered_programs |= program
        return filtered_programs


class SaleCouponReward(models.Model):
    _inherit = "sale.coupon.reward"

    reward_type = fields.Selection(selection_add=[("use_pricelist", "Pricelist")])


class SaleCoupon(models.Model):
    _inherit = "sale.coupon"

    reward_pricelist_id = fields.Many2one(
        related="program_id.reward_pricelist_id", string="Pricelist"
    )
