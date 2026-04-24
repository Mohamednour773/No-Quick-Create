# -*- coding: utf-8 -*-
{
    'name': 'ARM - Menu Hiding',
    'version': '19.0.1.0.0',
    'category': 'Technical / Security',
    'summary': 'Hide specific Odoo menu items per user access group at runtime.',
    'description': """
ARM - Menu Hiding
=================
Part of the Access Right Management (ARM) suite.

Features
--------
- Create named user access groups.
- Select menus to hide; child menus are automatically hidden too.
- No XML or system parameter changes required.
- Works with Odoo 19 native menu loading engine.
    """,
    'author': 'Mohamed Nour',
    'price': 10.0,
    'currency': 'USD',
    'license': 'OPL-1',
    'images': ['static/description/icon.svg'],
    'depends': ['base', 'web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/arm_group_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
