from odoo import models, fields

class LawCourt(models.Model):
    _name = 'law.court'
    _description = 'Law Court'

    name = fields.Char(string='Court Name', required=True)
    code = fields.Char(string='Court Code')
    address = fields.Text(string='Address')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')
