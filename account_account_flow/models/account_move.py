from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    mp_grupo_provicion_id = fields.Many2one(comodel_name="mp.grupo.provicion]")
    mp_provicion_id = fields.Many2one(comodel_name="mp.provicion", domain="[('id', 'in', mp_provicion_ids)]")
    # mp_provicion_ids = fields.One2many()#related="mp_grupo_provicion_id.mp_provicion_ids"

    # @api.onchange("mp_grupo_provicion_id")
    # def _onchange_mp_provicion_id(self):
    #     for move_io in self:
    #         move_io.mp_provicion_id = self.env['mp.provicion']