from odoo import models, fields, _, api


class Budget(models.Model):
    _name = 'h.budget'
    _inherit = ['mail.thread']

    name = fields.Char(string=_('name'), copy=False)
    total = fields.Monetary(string=_('Amount total'), compute='compute_total', store=True, tracking=True, currency_field='currency_id')
    expenses = fields.Monetary(string=_('Expenses'), compute='compute_expenses', store=True, currency_field='currency_id')
    remain = fields.Monetary(string=_('Remain'), compute='compute_remain', store=True, copy=False, tracking=True, currency_field='currency_id')
    income_ids = fields.One2many('h.income', 'budget_id', string=_('Income'))
    outcome_ids = fields.One2many('h.outcome', 'budget_id', string=_('Outcome'))
    currency_id = fields.Many2one('res.currency', string="Currency", default=172)

    @api.depends('income_ids')
    def compute_total(self):
        for record in self:
            record.total = 0
            if record.income_ids:
                record.total = sum(x.amount for x in record.income_ids)

    @api.depends('expenses', 'outcome_ids')
    def compute_expenses(self):
        for record in self:
            record.expenses = 0
            if record.outcome_ids:
                record.expenses = sum(x.amount for x in record.outcome_ids)

    @api.depends('expenses', 'total')
    def compute_remain(self):
        for record in self:
            record.remain = 0
            if record.total:
                record.remain = record.total - record.expenses

    def input_outcome(self):
        for record in self:
            res = {
                'type': 'ir.actions.act_window',
                'name': _('Outcome'),
                'res_model': 'h.outcome',
                'view_mode': 'form',
                'view_id': self.env.ref('control_spending_app.outcome_form').id,
                'context': {
                    'default_budget_id': record.id,
                }
            }
            return res

    def input_income(self):
        for record in self:
            res = {
                'type': 'ir.actions.act_window',
                'name': _('Income'),
                'res_model': 'h.income',
                'view_mode': 'form',
                'view_id': self.env.ref('control_spending_app.income_form').id,
                'context': {
                    'default_budget_id': record.id,
                }
            }
            return res

    def action_show_income(self):
        self.ensure_one()
        self = self.sudo()
        action = self.env.ref('control_spending_app.income_action').read()[0]
        action['domain'] = [
            ('budget_id', '=', self.id)
        ]
        action['context'] = {}
        return action

    def action_show_fee(self):
        self.ensure_one()
        self = self.sudo()
        action = self.env.ref('control_spending_app.outcome_action').read()[0]
        action['domain'] = [
            ('budget_id', '=', self.id)
        ]
        action['context'] = {}
        return action
