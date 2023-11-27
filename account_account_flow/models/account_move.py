from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    mp_grupo_provision_id = fields.Many2one(comodel_name="mp.grupo.provision]")
    mp_provision_id = fields.Many2one(comodel_name="mp.provision", domain="[('id', 'in', mp_provision_ids)]")
    # mp_provision_ids = fields.One2many()#related="mp_grupo_provision_id.mp_provision_ids"

    # @api.onchange("mp_grupo_provision_id")
    # def _onchange_mp_provision_id(self):
    #     for move_io in self:
    #         move_io.mp_provision_id = self.env['mp.provision']