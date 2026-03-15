from odoo import models, fields, api, _

class Lawyer(models.Model):
    _name = 'lawyer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Lawyer Management"

    employee_id = fields.Many2one('hr.employee', string='Employee')
    name = fields.Char(string="Name")
    mobile = fields.Char(string="Mobile")
    company_id = fields.Many2one('res.company')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    birth_date = fields.Date(string="Birth Date")
    image = fields.Binary("Image", attachment=True)
    practice_area_ids = fields.Many2many('practice.area', string="Practice Area")
    email = fields.Char(string="Email")
    active = fields.Boolean(default=True)
    case_ids = fields.One2many('lawyer.case', 'assigned_lawyer', string='Cases')
    legal_advice_ids = fields.One2many('legal.advice', 'lawyer_id', string='Legal Advice')
    
    case_count = fields.Integer(compute='_compute_case_count', string='Case Count')
    legal_advice_count = fields.Integer(compute='_compute_legal_advice_count', string='Legal Advice Count')

    @api.depends('case_ids')
    def _compute_case_count(self):
        for rec in self:
            rec.case_count = len(rec.case_ids)

    @api.depends('legal_advice_ids')
    def _compute_legal_advice_count(self):
        for rec in self:
            rec.legal_advice_count = len(rec.legal_advice_ids)

    def action_view_cases(self):
        self.ensure_one()
        return {
            'name': _('Cases'),
            'type': 'ir.actions.act_window',
            'res_model': 'lawyer.case',
            'view_mode': 'list,kanban,form',
            'domain': [('assigned_lawyer', '=', self.id)],
            'context': {'default_assigned_lawyer': self.id},
            'target': 'current',
        }

    def action_view_legal_advice(self):
        self.ensure_one()
        return {
            'name': _('Legal Advice'),
            'type': 'ir.actions.act_window',
            'res_model': 'legal.advice',
            'view_mode': 'list,form',
            'domain': [('lawyer_id', '=', self.id)],
            'context': {'default_lawyer_id': self.id},
            'target': 'current',
        }

    wage_type = fields.Selection([
        ('hourly', 'Hourly'),
        ('case', 'Per Case'),
        ('trial', 'Per Trial')
    ], string="Wage Type", default='case')
    wage_amount = fields.Float(string="Wage Amount")
