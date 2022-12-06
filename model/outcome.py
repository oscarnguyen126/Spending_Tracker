from odoo import models, fields, _, api
from datetime import datetime
from odoo.exceptions import ValidationError


class Outcome(models.Model):
    _name = 'h.outcome'
    _inherit = ['mail.thread']
    _rec_name = 'name'

    name = fields.Char(string=_('Name'), required=True, copy=False)
    amount = fields.Monetary(string=_('Amount'), currency_field='currency_id', required=True, tracking=True)
    outcome_date = fields.Date(string=_('Date'), required=True, tracking=True, default=datetime.now().strftime("%Y-%m-%d"))
    currency_id = fields.Many2one("res.currency", string=_("Currency"), default=172)
    budget_id = fields.Many2one('h.budget')
    category = fields.Many2one('h.category', string=_('Category'))

    @api.constrains('amount')
    def check_positive(self):
        for record in self:
            if record.amount < 0:
                raise ValidationError(_("The amount can't be negative"))

    def attach_document(self, **kwargs):
        pass
