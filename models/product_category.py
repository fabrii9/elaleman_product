import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProductCategory(models.Model):
    _inherit = 'product.category'

    sku_prefix = fields.Char(
        string='Prefijo SKU',
        help="Prefijo del SKU interno para los productos de esta categoría "
             "(ej. KF genera KF-0001, KF-0002...). Vacío: no se asigna SKU automático.",
    )

    _sql_constraints = [
        ('sku_prefix_uniq', 'unique(sku_prefix)', 'Ese prefijo de SKU ya lo usa otra categoría.'),
    ]

    @api.constrains('sku_prefix')
    def _check_sku_prefix(self):
        for categ in self.filtered('sku_prefix'):
            if not re.fullmatch(r'[A-Z0-9]+', categ.sku_prefix):
                raise ValidationError(_("El prefijo de SKU solo admite mayúsculas y números (ej. KF)."))

    def _next_sku_number(self):
        """Siguiente correlativo libre del prefijo, mirando también productos archivados."""
        self.ensure_one()
        pattern = re.compile(r'^%s-(\d+)$' % re.escape(self.sku_prefix))
        codes = self.env['product.product'].with_context(active_test=False).search_read(
            [('default_code', '=like', self.sku_prefix + '-%')], ['default_code'])
        numbers = [0]
        for code in codes:
            match = pattern.match(code['default_code'])
            if match:
                numbers.append(int(match.group(1)))
        return max(numbers) + 1

    def _next_sku(self):
        self.ensure_one()
        return '%s-%04d' % (self.sku_prefix, self._next_sku_number())

    def action_assign_missing_sku(self):
        """Asigna SKU a los productos activos de la categoría que todavía no tienen."""
        for categ in self.filtered('sku_prefix'):
            templates = self.env['product.template'].search(
                [('categ_id', '=', categ.id), ('default_code', '=', False)], order='name')
            for template in templates:
                template.default_code = categ._next_sku()
        return True
