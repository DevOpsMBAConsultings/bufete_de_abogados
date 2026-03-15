from odoo import models, fields, api, _

class LegalAdvice(models.Model):
    _name = 'legal.advice'
    _description = 'Legal Advice'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Client', required=True, tracking=True)
    date = fields.Date(string='Advice Date', default=fields.Date.context_today, tracking=True)
    lawyer_id = fields.Many2one('lawyer', string='Consulting Lawyer')
    practice_area_id = fields.Many2one('practice.area', string='Practice Area')
    description = fields.Text(string='Issue Description')
    advice_given = fields.Text(string='Advice Given')
    fee = fields.Float(string='Consultation Fee')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('converted', 'Converted to Case'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    case_id = fields.Many2one('lawyer.case', string='Related Case', readonly=True)
    service_line_ids = fields.One2many('legal.advice.service.line', 'advice_id', string='Service Lines')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('legal.advice') or _('New')
        return super().create(vals_list)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_create_case(self):
        self.ensure_one()
        case_vals = {
            'case_name': self.description or _('Case from Advice %s') % self.name,
            'partners_id': self.partner_id.id,
            'date': fields.Date.today(),
            'assigned_lawyer': self.lawyer_id.id,
            'case_type_id': self.practice_area_id.id,
            'description': self.advice_given,
        }
        case = self.env['lawyer.case'].create(case_vals)
        self.write({
            'state': 'converted',
            'case_id': case.id
        })
        return {
            'name': _('Case'),
            'type': 'ir.actions.act_window',
            'res_model': 'lawyer.case',
            'res_id': case.id,
            'view_mode': 'form',
            'target': 'current',
        }
