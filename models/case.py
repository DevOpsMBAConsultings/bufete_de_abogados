from odoo import models,fields,api ,_
from odoo.exceptions import ValidationError

class Case(models.Model):
    _name = 'lawyer.case'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Case"

    case_name = fields.Char(string="Case Name")
    description = fields.Text(string="Description")
    partners_id = fields.Many2one('res.partner', string="Customer", required=True)
    date = fields.Date(string="Date")
    assigned_lawyer = fields.Many2one('lawyer', string="Assigned lawyer")
    product_document_ids = fields.One2many('document', 'custom_model_id', string="Documents")
    partners_ids = fields.One2many('res.partner', 'lawyer_case_id', string="Partners")
    active = fields.Boolean(default=True)
    name = fields.Char(string="Order Reference",
                       required=True, copy=False,
                       readonly=True, index='trigram',
                       default=lambda self: _('New'))
    case_type_id = fields.Many2one('practice.area', string="Practice Area")
    stage_id = fields.Many2one('case.stage', string="Stage", tracking=True, 
                               default=lambda self: self.env['case.stage'].search([], limit=1),
                               group_expand='_read_group_stage_ids')
    date_of_judgment = fields.Datetime(string="Date of judgment")
    court_id = fields.Many2one('law.court', string="Court")
    judge_id = fields.Many2one('law.judge', string="Judge")
    court_docket_number = fields.Char(string="Court Docket Number")
    hearing_ids = fields.One2many('hearing.case', 'hearing_id', string="Hearing")
    service_line_ids = fields.One2many('lawyer.case.service.line', 'case_id', string="Service Lines")
    sale_order_id = fields.Many2one('sale.order', string="Linking Quotation", readonly=True)
    amount_total = fields.Monetary(string="Total Amount", compute='_compute_amount_total', store=True, currency_field='currency_id', aggregator="sum")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    kanban_state = fields.Selection([
        ('normal', 'Grey'),
        ('done', 'Green'),
        ('blocked', 'Red')], string='Kanban State', default='normal')

    @api.depends('service_line_ids.subtotal')
    def _compute_amount_total(self):
        for case in self:
            case.amount_total = sum(line.subtotal for line in case.service_line_ids)

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        return self.env['case.stage'].search([])

    @api.constrains('stage_id', 'assigned_lawyer')
    def _check_assigned_lawyer(self):
        for rec in self:
            if rec.stage_id and rec.stage_id.name == 'Work in Progress' and not rec.assigned_lawyer:
                raise ValidationError("You must assign a lawyer when the case is in 'Work in Progress' state.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code('lawyer.case') or _("New")
        return super().create(vals_list)

    def action_work_in_progress(self):
        wip_stage = self.env['case.stage'].search([('name', '=', 'Work in Progress')], limit=1)
        if wip_stage:
            self.write({'stage_id': wip_stage.id})

    def action_done(self):
        done_stage = self.env['case.stage'].search([('name', '=', 'Done')], limit=1)
        if done_stage:
            self.write({'stage_id': done_stage.id})

    def action_closed(self):
        closed_stage = self.env['case.stage'].search([('is_closed', '=', True)], limit=1)
        if closed_stage:
            self.write({'stage_id': closed_stage.id})

    def action_create_quotation(self):
        self.ensure_one()
        if self.sale_order_id:
            raise ValidationError(_("A quotation already exists for this case."))
        
        order_lines = []
        for line in self.service_line_ids:
            order_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.name,
                'product_uom_qty': line.quantity,
                'price_unit': line.price_unit,
            }))
        
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partners_id.id,
            'assigned_lawyer': self.assigned_lawyer.id,
            'order_line': order_lines,
            'origin': self.name,
        })
        self.sale_order_id = sale_order.id
        return True

    def action_update_quotation(self):
        self.ensure_one()
        if not self.sale_order_id:
            return False
        
        if self.sale_order_id.state not in ['draft', 'sent']:
            # If called manually, we might want to warn, but if called via write(), we just skip
            return False

        # Clear existing lines and re-sync
        self.sale_order_id.order_line.unlink()
        order_lines = []
        for line in self.service_line_ids:
            order_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.name,
                'product_uom_qty': line.quantity,
                'price_unit': line.price_unit,
            }))
        self.sale_order_id.write({'order_line': order_lines})
        return True

    def write(self, vals):
        res = super(Case, self).write(vals)
        if 'service_line_ids' in vals:
            for rec in self:
                if rec.sale_order_id:
                    rec.action_update_quotation()
        return res

    def action_view_quotation(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': self.sale_order_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model
    def get_dashboard_stats(self, lawyer_id=None, date_range=None):
        domain = []
        advice_domain = []
        hearing_domain = []
        invoice_domain = [('move_type', '=', 'out_invoice')]

        if lawyer_id:
            domain.append(('assigned_lawyer', '=', lawyer_id))
            advice_domain.append(('lawyer_id', '=', lawyer_id))
            # Hearings are linked to cases via hearing_id, so we filter by case.assigned_lawyer
            hearing_domain.append(('hearing_id.assigned_lawyer', '=', lawyer_id))
            # Invoices are created via action_done, let's keep it simple for now as they are linked to partner
            # If we need lawyer-specific invoice stats, we might need a link on account.move

        # In a real app, date_range would be handled here
        # For now, we fetch all stats

        return {
            'advice': {
                'total': self.env['legal.advice'].search_count(advice_domain),
                'new': self.env['legal.advice'].search_count(advice_domain + [('state', '=', 'draft')]),
                'closed': self.env['legal.advice'].search_count(advice_domain + [('state', 'in', ['converted', 'cancelled'])]),
            },
            'cases': {
                'total': self.search_count(domain),
                'won': self.search_count(domain + [('hearing_ids.result', '=', 'won')]),
            },
            'hearings': {
                'total': self.env['hearing.case'].search_count(hearing_domain),
                'new': self.env['hearing.case'].search_count(hearing_domain + [('result', '=', 'pending')]),
                'open': self.env['hearing.case'].search_count(hearing_domain + [('result', '=', 'pending')]),
                'closed': self.env['hearing.case'].search_count(hearing_domain + [('result', 'in', ['won', 'lost'])]),
            },
            'invoices': {
                'total': self.env['account.move'].search_count(invoice_domain),
                'paid': self.env['account.move'].search_count(invoice_domain + [('payment_state', '=', 'paid')]),
                'due': self.env['account.move'].search_count(invoice_domain + [('payment_state', 'in', ['not_paid', 'partial'])]),
            },
        }










