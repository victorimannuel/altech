# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MaterialMaterial(models.Model):
    _name = "material.material"
    _description = "Material"
    _order = 'code asc'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton')
    ], 'Type', default='fabric', required=True)
    buy_price = fields.Integer(string='Buy Price', required=True)
    supplier_id = fields.Many2one('res.partner', string='Related Supplier', required=True)

    @api.constrains('buy_price')
    def _check_value(self):
        if self.buy_price < 100:
            raise ValidationError(_('Enter buy price greater equal than 100'))

