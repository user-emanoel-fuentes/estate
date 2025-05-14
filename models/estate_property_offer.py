from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float('price')
    
    status = fields.Selection([
        ('accepeted', 'Accepeted'),
        ('refused', 'Refused'),
    ], string='status', copy=False)

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    validity = fields.Integer(string="Validity", default=7)

    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Date Deadline")
    
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self: 
            record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days