from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char(string='SKU interno')

    @api.constrains('default_code')
    def _check_default_code_unique(self):
        for product in self.filtered('default_code'):
            duplicate = self.with_context(active_test=False).search([
                ('default_code', '=', product.default_code),
                ('id', '!=', product.id),
            ], limit=1)
            if duplicate:
                raise ValidationError(_(
                    "El SKU interno %(code)s ya lo usa el producto %(product)s.",
                    code=product.default_code, product=duplicate.display_name))
