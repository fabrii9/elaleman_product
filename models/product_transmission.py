from odoo import fields, models


class ProductTransmission(models.Model):
    _name = 'product.transmission'
    _description = 'Código de transmisión'
    _order = 'name'

    name = fields.Char(string='Código', required=True)
    active = fields.Boolean(default=True)
    product_count = fields.Integer(string='Productos', compute='_compute_product_count')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Ese código de transmisión ya existe.'),
    ]

    def _compute_product_count(self):
        data = self.env['product.template']._read_group(
            [('transmission_ids', 'in', self.ids)], ['transmission_ids'], ['__count'])
        counts = {transmission.id: count for transmission, count in data}
        for transmission in self:
            transmission.product_count = counts.get(transmission.id, 0)
