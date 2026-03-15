from odoo import fields, models, api, _

class CustomerPartner(models.Model):
    _inherit = 'res.partner'

    #field relation between res partner and case model
    is_law_client = fields.Boolean(string="Client", default=False)
    lawyer_case_id = fields.Many2one('lawyer.case', string="Lawyer Case")
    case_count = fields.Integer(compute='_compute_case_counts', string="Cases Count")
    advice_count = fields.Integer(compute='_compute_advice_counts', string="Advice Count")

    def _compute_case_counts(self):
        for rec in self:
            rec.case_count = self.env['lawyer.case'].search_count([('partners_id', '=', rec.id)])

    def _compute_advice_counts(self):
        for rec in self:
            rec.advice_count = self.env['legal.advice'].search_count([('partner_id', '=', rec.id)])

    def action_view_cases(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cases'),
            'view_mode': 'list,kanban,form',
            'res_model': 'lawyer.case',
            'domain': [('partners_id', '=', self.id)],
            'context': {'default_partners_id': self.id},
            'target': 'current',
        }

    def action_view_legal_advice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Legal Advice'),
            'view_mode': 'list,form',
            'res_model': 'legal.advice',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
            'target': 'current',
        }
