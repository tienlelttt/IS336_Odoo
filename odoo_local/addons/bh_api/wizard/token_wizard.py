from odoo import fields, models


class BhApiTokenWizard(models.TransientModel):
    _name = "bh.api.token.wizard"
    _description = "Hiển thị token mới (một lần)"

    client_id = fields.Many2one("bh.api.client", readonly=True)
    token = fields.Char(readonly=True)
