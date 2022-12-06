from odoo import models, fields, api, _


class Category(models.Model):
    _name = 'h.category'

    name = fields.Char(string=_('Category'), required=True)
