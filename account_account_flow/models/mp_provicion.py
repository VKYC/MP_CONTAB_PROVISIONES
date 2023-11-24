from odoo import fields, models


class MpProvicion(models.Model):
    _name = 'mp.provicion'
    _rec_name = "codigo"

    codigo = fields.Char()
    decripcion = fields.Text()
    cuanta_gasto_id = fields.Many2one(comodel_name="account.account", domain="[('account_type', '=', 'expense')]")
    cuanta_pasivo_id = fields.Many2one(comodel_name="account.account", domain="[('account_type', '=', 'passive')]")
    mp_grupo_provicion_ids = fields.Many2many(comodel_name="mp.grupo.provicion", string="Grupo Provicion")

    mp_grupo_provicion_id = fields.Many2one(comodel_name="mp.grupo.flujo")
