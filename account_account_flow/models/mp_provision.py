from odoo import fields, models, _, api


class MpProvision(models.Model):
    _name = 'mp.provision'
    _rec_name = "codigo"

    codigo = fields.Char(readonly=True, required=True, copy=False, default=lambda self: _('New'))
    decripcion = fields.Text()
    cuenta_gasto_id = fields.Many2one(comodel_name="account.account", domain="[('account_type', '=', 'expense')]")
    cuenta_pasivo_id = fields.Many2one(comodel_name="account.account", domain="[('account_type', '=', 'passive')]")
    mp_grupo_provision_ids = fields.Many2many(comodel_name="mp.grupo.provision", string="Grupo Provision")

    mp_grupo_provision_id = fields.Many2one(comodel_name="mp.grupo.flujo")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')):
            vals['codigo'] = self.env['ir.sequence'].sudo().next_by_code('mp.provision')
        return super(MpProvision, self).create(vals)
