from odoo import fields, models, api
from odoo.tools.translate import _


class PropertyType(models.Model):
    _name="estate.property.type"
    _description="Type of real estate model"
    _order = "sequence desc"

    sequence = fields.Integer(default=1)
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    property_count = fields.Integer(compute="_compute_property_count")



    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for vals in vals_list:
            self.env["estate.property.tag"].create(
                {
                    "name": vals.get("name"),
                }
            )
        return res

    def unlink(self):
        self.property_ids.state = "cancelled"
        return super().unlink()

    @api.depends("property_ids")
    def _compute_property_count(self):
        for rec in self:
            rec.property_count = len(rec.property_ids)


    def action_open_property_ids(self):
        return{
            "name": _("Related Properties"),
            "type": "ir.actions.act_window",
            "res_model": "estate.property",
            "view_mode": "list,form",
            "target": "current",
            "domain": [("property_type_id", "=", self.id)],
            "context": {"default_property_type_id": self.id},
        }
