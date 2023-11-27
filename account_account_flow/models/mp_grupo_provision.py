from odoo import fields, models


class MpGrupoProvision(models.Model):
    _name = 'mp.grupo.provision'
    _rec_name = "nombre"

    nombre = fields.Char()
    descripcion = fields.Text()

    mp_provision_ids = fields.One2many(comodel_name="mp.provision", inverse_name="mp_grupo_provision_id",
                                       compute="_compute_mp_provision_ids")

    def _compute_mp_provision_ids(self):
        for grupo_id in self:
            provision_ids = self.env["mp.provision"].search([("mp_grupo_provision_ids", "=", grupo_id.id)])
            for provision_id in provision_ids:
                grupo_id.mp_provision_ids += provision_id

