# -*- coding: utf-8 -*-
{
    'name': 'Library Management',
    'version': '1.0',
    'summary': 'Manage library books, members and checkouts',
    'description': '''
        * Manage book catalog
        * Register library members
        * Track book checkouts and returns
        * Control book availability
    ''',
    'category': 'Services',
    'author': 'fgaviiria',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
		'views/library_book_views.xml',
		'views/library_member_views.xml',
		'views/library_checkout_views.xml',
		'views/library_menu.xml',
],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}