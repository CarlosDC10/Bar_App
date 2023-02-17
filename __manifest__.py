# -*- coding: utf-8 -*-
{
    'name': "bar_app",

    'summary': """
        Menu application for Ca La Luna""",

    'description': """
        Menu application where you can controll the products of the menu
    """,

    'author': "Carlos Duato",
    'website': "http://www.isca.es",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/bar_group_security.xml',
        'security/ir.model.access.csv',
        'views/category_view.xml',
        'views/product_view.xml',
        'views/ingredient_view.xml',
        'views/table_view.xml',
        'views/productQuant_view.xml',
        'views/productq_view_cook.xml',
        'views/productq_view_barman.xml',
        'views/productq_view_waiter.xml',
        'views/invoice_view.xml',
        'views/invoiceProd_view.xml',
        'views/menu.xml',
        'report/invoice_report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True
}
