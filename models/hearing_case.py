from odoo import models, fields, api, _

class HearingCase(models.Model):
    _name = 'hearing.case'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hearing Case"

    scheduling_date= fields.Datetime(string="Scheduling Date")
    party_id = fields.Many2one('res.partner', string="Party")
    note = fields.Char(string="Note")
    hearing_id = fields.Many2one('lawyer.case')
    evidence_description = fields.Text(string="Evidence Details")
    witness_ids = fields.Many2many('res.partner', string="Witnesses")
    judgment = fields.Text(string="Judgment/Decision")
    result = fields.Selection([
        ('pending', 'Pending'),
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('postponed', 'Postponed')
    ], string="Result", default='pending')






