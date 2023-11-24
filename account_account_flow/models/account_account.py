from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit = "account.account"

    account_type = fields.Selection(
        selection=[("passive", "Es cuenta pasivos"), ("expense", "Es cuenta de gastos")],
        string="Tipo de cuenta"
    )
