from odoo import models, fields

class CaseStage(models.Model):
    _name = 'case.stage'
    _description = 'Case Stage'
    _order = 'sequence, id'

    name = fields.Char(string='Stage Name', required=True, translate=True)
    sequence = fields.Integer(default=1)
    is_closed = fields.Boolean(string='Closed Stage', default=False)
    description = fields.Text(string='Description')
