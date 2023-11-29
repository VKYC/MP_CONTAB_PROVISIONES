from odoo import fields, models, api


class MpProvisionJournalItem(models.Model):
    _name = 'mp.provision.journal.item'
    _rec_name = 'account_id'

    account_id = fields.Many2one(comodel_name='account.account', string='Cuenta')
    debit = fields.Monetary(string='Debito', currency_field="currency_id")
    credit = fields.Monetary(string='Credito', currency_field="currency_id")
    mp_provision_account_move_id = fields.Many2one(comodel_name='mp.provision.account.move')
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency of the Payment Transaction",
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )

    @api.onchange('debit')
    def onchange_debit(self):
        for item in self:
            if item.debit != 0:
                item.credit = 0

    @api.onchange('credit')
    def onchange_credit(self):
        for item in self:
            if item.credit != 0:
                item.debit = 0
