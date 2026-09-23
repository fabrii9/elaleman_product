from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    default_code = fields.Char(string='SKU interno')
    transmission_ids = fields.Many2many(
        'product.transmission', 'product_template_transmission_rel',
        'product_tmpl_id', 'transmission_id', string='Código de transmisión',
        help="Cajas de transmisión para las que sirve el repuesto (ej. U340, U341).",
    )
    condition = fields.Selection(
        [('nuevo', 'Nuevo'), ('usado', 'Usado'), ('reman', 'Remanufacturado')],
        string='Estado', tracking=True,
    )
    supplier_sku = fields.Char(
        string='SKU proveedor',
        help="Código original del proveedor o del fabricante (ej. YH303, 901064).",
    )
    legacy_code = fields.Char(
        string='Referencia anterior', copy=False,
        help="Referencia interna que tenía el producto antes de pasar al SKU interno nuevo.",
    )
    purchase_status = fields.Selection(
        [('activo', 'Activo'), ('no_recomprar', 'No recomprar')],
        string='Estado de compra', default='activo', required=True, tracking=True,
        help="No recomprar: se sigue vendiendo hasta agotar stock, pero no se "
             "puede comprar ni aparece en las sugerencias de reposición.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('purchase_status') == 'no_recomprar':
                vals['purchase_ok'] = False
        templates = super().create(vals_list)
        templates.filtered(lambda t: not t.default_code)._assign_sku_from_category()
        return templates

    def write(self, vals):
        if 'purchase_status' in vals:
            vals = dict(vals, purchase_ok=vals['purchase_status'] == 'activo')
        res = super().write(vals)
        if vals.get('purchase_status') == 'no_recomprar':
            self._archive_orderpoints()
        if 'categ_id' in vals:
            self.filtered(lambda t: not t.default_code)._assign_sku_from_category()
        return res

    def _assign_sku_from_category(self):
        # Solo productos sin variantes: con variantes cada una lleva su propio SKU.
        # 'skip_sku_auto' lo usan las cargas masivas que traen el SKU ya definido.
        if self.env.context.get('skip_sku_auto'):
            return
        for template in self:
            if template.categ_id.sku_prefix and template.product_variant_count <= 1:
                template.default_code = template.categ_id._next_sku()

    def _archive_orderpoints(self):
        orderpoints = self.env['stock.warehouse.orderpoint'].search(
            [('product_id', 'in', self.product_variant_ids.ids)])
        orderpoints.write({'active': False})
