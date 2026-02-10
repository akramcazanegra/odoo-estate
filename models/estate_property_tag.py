from odoo import fields, models
import random

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of Real Estate Model"
    _sql_constraints = [
        ("unique_tag","UNIQUE(name)","tag should be unique")
    ]
    _order = "name asc"


    name = fields.Char(required=True)
    #color = fields.Integer(default=1)
    color = fields.Integer(default=lambda self: random.randint(1, 11))