from odoo import models, fields, api

class LegalAdviceServiceLine(models.Model):
    _name = 'legal.advice.service.line'
    _description = 'Legal Advice Service Line'

    advice_id = fields.Many2one('legal.advice', string='Legal Advice', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Service', domain=[('type', '=', 'service')], required=True)
    name = fields.Text(string='Description', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.get_product_multiline_description_sale()
            self.price_unit = self.product_id.list_price

class LawyerCaseServiceLine(models.Model):
    _name = 'lawyer.case.service.line'
    _description = 'Lawyer Case Service Line'

    case_id = fields.Many2one('lawyer.case', string='Case', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Service', domain=[('type', '=', 'service')], required=True)
    name = fields.Text(string='Description', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price')
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.get_product_multiline_description_sale()
            self.price_unit = self.product_id.list_price
