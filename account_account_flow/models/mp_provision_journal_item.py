from odoo import fields, models, api


class MpProvisionJournalItem(models.Model):
    _name = 'mp.provision.journal.item'
    _rec_name = 'account_id'
    _order = "mp_provision_id DESC"

    account_id = fields.Many2one(comodel_name='account.account', string='Cuenta')
    debit = fields.Monetary(string='Debito', currency_field="currency_id")
    credit = fields.Monetary(string='Credito', currency_field="currency_id")
    mp_provision_account_move_id = fields.Many2one(comodel_name='mp.provision.account.move', string='Provision')
    analytic_tag_ids = fields.Many2many(related='mp_provision_account_move_id.analytic_tag_ids')
    analytic_account_id = fields.Many2one(related='mp_provision_account_move_id.analytic_account_id')
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency of the Payment Transaction",
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )
    state = fields.Selection(related='mp_provision_account_move_id.state')
    date = fields.Date(related='mp_provision_account_move_id.date')
    mp_provision_id = fields.Many2one(related='mp_provision_account_move_id.mp_provision_id', store=True)

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
