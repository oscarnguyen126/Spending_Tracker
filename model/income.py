from odoo import models, fields, _, api
from datetime import datetime
from odoo.exceptions import ValidationError


class Income(models.Model):
    _name = 'h.income'
    _inherit = ['mail.thread']
    _rec_name = 'name'

    name = fields.Char(string=_('Name'), required=True, copy=False)
    amount = fields.Monetary(string=_('Amount'), currency_field='currency_id', required=True, tracking=True)
    income_date = fields.Date(string=_('Date'), required=True, tracking=True, default=datetime.now().strftime("%Y-%m-%d"))
    currency_id = fields.Many2one('res.currency', string='Currency', default=172)
    budget_id = fields.Many2one('h.budget')

    @api.constrains('amount')
    def check_positive(self):
        for record in self:
            if record.amount < 0:
                raise ValidationError(_("The amount can't be negative"))
