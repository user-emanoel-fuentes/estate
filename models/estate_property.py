from odoo import models, fields, api


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char('name', required=True)

    description = fields.Text('description')

    postcode = fields.Char('postcode')

    def get_date(self):
        today = fields.date.today()
        return today.replace(month=today.month + 3)

    date_availability = fields.Date('date_availability', copy=False, default=get_date)

    expected_price = fields.Float('expected_price', required=True)

    selling_price = fields.Float('selling_price', readonly=True)

    bedrooms = fields.Integer('bedrooms', default=2)

    living_area = fields.Integer('living_area')

    facades = fields.Integer('facades')

    garage = fields.Boolean('garage')

    garden = fields.Boolean('garden')

    garden_area = fields.Integer('garden_area')

    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string='Garden Orientation')

    active = fields.Boolean(string='Active', default=True)

    state = fields.Selection([
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string='State', default='new', copy=False, required=True,)

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')

    buyer_id = fields.Many2one('res.partner', string='Buyer')

    salesperson_id = fields.Many2one('res.users', string='Salesperson')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    tag_ids = fields.Many2many('estate.property.tag', string="Tags")

    total_area = fields.Float(compute="_compute_total_area", string="Total Area", readonly=True)

    best_price = fields.Float(compute="_compute_best_price", string="Best Price", readonly=True)

    # METHODS

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self: 
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"))

    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.write({
                    "garden_area" : 10,
                    "garden_orientation" : "north"
                })
            else:
                record.write({
                    "garden_area" : 0,
                    "garden_orientation" : None
                })

    @api.onchange("date_availability")
    def _onchange_date_availability(self):
        for record in self:
            if record.date_availability < fields.Date.today():
                return {
                    "warning" : {
                        "title" : ("Warning"),
                        "message" : "Availability date provided precedes current date."
                    }
                }
    
    