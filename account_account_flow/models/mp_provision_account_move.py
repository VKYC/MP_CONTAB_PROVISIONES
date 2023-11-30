from odoo import fields, models, api, _


class MpProvisionAccountMove(models.Model):
    _name = 'mp.provision.account.move'
    _order = "name DESC"

    name = fields.Char(readonly=True, required=True, copy=False, default=lambda self: _('New'))
    date = fields.Date(required=True, string='Fecha')
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmado"),
        ],
        default="draft",
    )
    mp_grupo_provision_id = fields.Many2one(comodel_name='mp.grupo.provision', string='MP Grupo Provision',
                                            required=True)
    mp_provision_id = fields.Many2one(comodel_name='mp.provision', string='MP Provision',
                                      domain="[('id', 'in', mp_provision_ids)]", required=True)
    mp_provision_ids = fields.One2many(related="mp_grupo_provision_id.mp_provision_ids")
    analytic_account_id = fields.Many2one('account.analytic.account', string='Cuenta Analitica',
                                          index=True, check_company=True, copy=True)
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Tags Analiticas',
                                        store=True, readonly=False, check_company=True, copy=True)
    mp_provision_journal_item_ids = fields.One2many(comodel_name='mp.provision.journal.item',
                                                    inverse_name='mp_provision_account_move_id')
    account_move_id = fields.Many2one(comodel_name='account.move', string='Apunte de Diario')
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency of the Payment Transaction",
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )

    def write(self, vals):
        res = super(MpProvisionAccountMove, self).write(vals)
        list_line_ids = []
        sequence = 0
        for line_id in self.mp_provision_journal_item_ids:
            amount_currency = line_id.debit if line_id.credit == 0 else line_id.credit
            amount_currency = amount_currency * -1 if line_id.credit != 0 else amount_currency
            list_line_ids.append(
                (0, 0, {
                    'account_id': line_id.account_id.id,
                    'account_root_id': line_id.account_id.id,
                    'name': line_id.account_id.name,
                    'display_type': False,
                    'debit': line_id.debit,
                    'credit': line_id.credit,
                    'sequence': sequence,
                    'amount_currency': amount_currency,
                    'currency_id': self.currency_id.id,
                    'analytic_account_id': self.analytic_account_id.id,
                    'analytic_tag_ids': self.analytic_tag_ids.ids,
                    'company_currency_id': self.currency_id.id,
                    'quantity': 1,
                    'product_id': False,
                })
            )
            sequence += 1
        self.account_move_id.line_ids.unlink()
        self.account_move_id.sudo().write({'line_ids': list_line_ids})
        self.account_move_id.sudo().write({'date': self.date})
        return res

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')):
            provision_move_ids = self.env['mp.provision.account.move'].sudo().search([('name', 'ilike', 'PROV%')])
            current_date = fields.Datetime.now()
            if not provision_move_ids:
                vals['name'] = f"PROV/{current_date.year}/{current_date.month}/1"
            else:
                vals['name'] = f"PROV/{current_date.year}/{current_date.month}/{len(provision_move_ids)}"

        rec = super(MpProvisionAccountMove, self).create(vals)

        journal_id = self.env['account.journal'].search([('code', 'ilike', 'vario')])
        rec.account_move_id = self.env['account.move'].sudo().create({
            'state': 'draft',
            'date': rec.date,
            'journal_id': journal_id.id,
            'name': rec.name,
        })
        list_line_ids = []
        sequence = 0
        for line_id in rec.mp_provision_journal_item_ids:
            amount_currency = line_id.debit if line_id.credit == 0 else line_id.credit
            amount_currency = amount_currency * -1 if line_id.credit != 0 else amount_currency
            list_line_ids.append(
                (0, 0, {
                    'account_id': line_id.account_id.id,
                    'account_root_id': line_id.account_id.id,
                    'name': line_id.account_id.name,
                    'display_type': False,
                    'debit': line_id.debit,
                    'credit': line_id.credit,
                    'sequence': sequence,
                    'amount_currency': amount_currency,
                    'currency_id': rec.currency_id.id,
                    'analytic_account_id': rec.analytic_account_id.id,
                    'analytic_tag_ids': rec.analytic_tag_ids.ids,
                    'company_currency_id': rec.currency_id.id,
                    'quantity': 1,
                    'product_id': False,
                })
            )
            sequence += 1
        rec.account_move_id.sudo().write({'line_ids': list_line_ids})
        return rec

    def action_confirm(self):
        self.state = 'confirmed'
        self.account_move_id.action_post()

    @api.onchange('mp_provision_id')
    def onchange_mp_provision_id(self):
        for provision_id in self:
            provision_id.mp_provision_journal_item_ids = self.env['mp.provision.journal.item']
            if provision_id.mp_provision_id.cuenta_gasto_id:
                provision_id.mp_provision_journal_item_ids += self.env['mp.provision.journal.item'].create({
                    'account_id': provision_id.mp_provision_id.cuenta_gasto_id.id,
                    'debit': 0,
                    'credit': 0,
                })
            if provision_id.mp_provision_id.cuenta_pasivo_id:
                provision_id.mp_provision_journal_item_ids += self.env['mp.provision.journal.item'].create({
                    'account_id': provision_id.mp_provision_id.cuenta_pasivo_id.id,
                    'debit': 0,
                    'credit': 0,
                })
