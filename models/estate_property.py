from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta

class RealEstate(models.Model):
    _name = "estate.property"
    _description = "Real Estate Model"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    price = fields.Float()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    postcode = fields.Char()
    date_availability = fields.Date(default=fields.Date.today)
    expected_price = fields.Float()
    best_offer = fields.Float(compute="_compute_best_offer",store=True, group_operator="max" )
    selling_price = fields.Float()
    description = fields.Text()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
    property_type_id = fields.Many2one("estate.property.type")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for prop in self:
            prop.best_offer = max(prop.offer_ids.mapped('price')) if prop.offer_ids else 0.0

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = (prop.living_area or 0) + (prop.garden_area or 0)

    @api.onchange('garden')
    def _onchange_garden(self):
        for estate in self:
            if not estate.garden:
                estate.garden_area = 0

    @api.onchange('date_availability')
    def _onchange_date_availability(self):
        for estate in self:
            if estate.date_availability and estate.date_availability < fields.Date.today():
                return {
                    'warning': {
                        'title': _("Incorrect date"),
                        'message': _("The availability date cannot be set in the past."),
                    },
                }

    def action_cancel(self):
        self.ensure_one()
        if self.state == "sold":
            raise UserError(_("A sold property cannot be canceled."))
        self.state = "canceled"

    def action_sold(self):
        self.ensure_one()

        if self.state == "canceled":
            raise UserError(_("A canceled property cannot be sold."))

        if self.selling_price < 5000:
            raise ValidationError(_("The selling price must be at least 5000."))

        self.state = "sold"


   # @api.constrains("selling_price")
    #def _check_constraint(self):
     #   for estate in self:
      #      if estate.selling_price < 5000:
       #         raise ValidationError(_("The selling price must be at least 5000."))

    @api.constrains('selling_price', 'state')
    def _check_selling_price(self):
        for record in self:
            if record.state == 'sold' and record.selling_price < 5000:
                raise ValidationError(_("The selling price must be at least 5000"))



    def _cron_cancel_properties(self, limit=300):
        today = fields.Date.today()
        domain = [
            ('state', '=', 'new'),
            ('date_availability', '<', today)
        ]
        
        records = self.search(domain, limit=limit)
        
        if records:
            records.write({'state': 'canceled'})
        
        remaining = 0 if len(records) < limit else self.search_count(domain)
        self.env['ir.cron']._commit_progress(len(records), remaining=remaining)

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # 2. La fonction dial le Smart Button
    def action_open_offers(self):
        context = {'default_property_id': self.id}
        # Task: Ila kan Admin, default price > 5000
        if self.env.user.has_group('base.group_system'):
           context.update({'default_price': 5001})

        if self.best_offer > 5000:
           context.update({'is_danger_price': True})
            
        return {
            "name": _("Property Offers"),
            "type": "ir.actions.act_window",
            "res_model": "estate.property.offer",
            "view_mode": "list,form",
            "domain": [("property_id", "=", self.id)],
            "context": context,
        }

   