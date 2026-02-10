from odoo import models, fields, api


class PropertyOffer(models.Model):
    _inherit = "estate.property.offer"


    account_move_id = fields.Many2one("account.move")