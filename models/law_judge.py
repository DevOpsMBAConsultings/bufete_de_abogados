from odoo import models, fields

class LawJudge(models.Model):
    _name = 'law.judge'
    _description = 'Law Judge'

    name = fields.Char(string='Judge Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Related Partner')
    bio = fields.Text(string='Biography')
    practice_area_ids = fields.Many2many('practice.area', string='Expertise')
