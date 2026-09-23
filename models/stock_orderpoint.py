from odoo import models


class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'

    def _get_orderpoint_products(self):
        # Los productos "No recomprar" no deben aparecer como sugerencia de reposición.
        products = super()._get_orderpoint_products()
        return products.filtered(lambda p: p.purchase_status != 'no_recomprar')
