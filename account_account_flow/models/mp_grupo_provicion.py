from odoo import fields, models


class MpGrupoProvicion(models.Model):
    _name = 'mp.grupo.provicion'
    _rec_name = "nombre"

    nombre = fields.Char()
    descripcion = fields.Text()

    mp_provicion_ids = fields.One2many(comodel_name="mp.provicion", inverse_name="mp_grupo_provicion_id",
                                       compute="_compute_mp_provicion_ids")

    def _compute_mp_provicion_ids(self):
        for grupo_id in self:
            provicion_ids = self.env["mp.provicion"].search([("mp_grupo_provicion_ids", "=", grupo_id.id)])
            for provicion_id in provicion_ids:
                grupo_id.mp_provicion_ids += provicion_id

