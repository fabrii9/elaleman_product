{
    'name': 'El Alemán - Ficha de Repuestos',
    'version': '18.0.1.1.1',
    'category': 'Inventory/Inventory',
    'summary': 'SKU interno automático por categoría, código de transmisión, estado del repuesto, SKU de proveedor y estado de compra.',
    'description': """
        Personalizaciones de la ficha de producto para El Alemán:

        - La Referencia interna nativa pasa a llamarse "SKU interno".
        - Cada categoría puede tener un prefijo de SKU (KF, KJ, KA...). Al crear
          un producto en esa categoría (o al pasarlo a ella sin SKU) se le asigna
          el siguiente correlativo: KF-0001, KF-0002...
        - Campo "Código de transmisión" (etiquetas, admite varias cajas por producto).
        - Campo "Estado" del repuesto: Nuevo / Usado / Remanufacturado.
        - Campo "SKU proveedor" (código original del proveedor / fabricante).
        - Campo "Referencia anterior" para conservar el código previo al cambio de SKU.
        - Campo "Estado de compra": Activo / No recomprar. "No recomprar" quita el
          tilde nativo "Se puede comprar", archiva las reglas de reabastecimiento
          del producto y lo excluye de las sugerencias de reposición.
        - Foto del producto: clic para verla en grande (visor con zoom y descarga).
    """,
    'author': 'Aftermoves',
    'depends': ['product', 'sale', 'purchase_stock', 'custom_product_brand'],
    'data': [
        'security/ir.model.access.csv',
        'data/sku_label.xml',
        'views/product_transmission_views.xml',
        'views/product_category_views.xml',
        'views/product_template_views.xml',
        'views/product_product_views.xml',
        'views/product_image_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'elaleman_product/static/src/image_lightbox/*',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
