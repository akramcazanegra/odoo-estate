from odoo import models, fields, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo.tools.translate import _


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers made for real estates"

    price = fields.Float()
    status = fields.Selection(
        [("new", "New"), ("accepted", "Accepted"), ("refused", "Refused")],
        default="new",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def action_accept(self):
        self.ensure_one()
        if "accepted" in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("This property already has an accepted offer."))
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.state = "accepted"
       

    def action_refuse(self):
        for offer in self:
            #offer.status = "refused"
            offer.write({'status': 'refused'})

 
    
  

        
