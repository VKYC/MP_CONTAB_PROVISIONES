from odoo import fields, models


class MpProvision(models.Model):
    _name = 'mp.provision'
    _rec_name = "codigo"

    codigo = fields.Char()
    decripcion = fields.Text()
    cuanta_gasto_id = fields.Many2one(comodel_name="account.account", domain="[('account_type', '=', 'expense')]")
    cuanta_pasivo_id = fields.Many2one(comodel_name="account.account", domain="[('account_type', '=', 'passive')]")
    mp_grupo_provision_ids = fields.Many2many(comodel_name="mp.grupo.provision", string="Grupo Provision")

    mp_grupo_provision_id = fields.Many2one(comodel_name="mp.grupo.flujo")
