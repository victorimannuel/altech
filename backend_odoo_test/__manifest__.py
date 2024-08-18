# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Backend Odoo Test',
    'version': '1.0',
    'category': '',
    'summary': 'Module for backend odoo test',
    'description': 'Module for backend odoo test',
    'depends': [],
    # 'images' : ['images/accounts.jpeg']
    'data': [
        # 'data/adyen_platforms_data.xml',
        'security/ir.model.access.csv',
        'views/material_views.xml',
    ],
    'qweb': [
    ],
    'application': True,
    'auto_install': False,
    'installable': True,
    'license': 'LGPL-3',
}
