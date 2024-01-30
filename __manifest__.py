# -*- coding: utf-8 -*-
{
    'name': 'Hotel',
    'version': '',
    'description': """ Módulo de gestión hotelera """,
    'summary': """ Módulo que brinda herramientas para la gestión de un hotel """,
    'author': 'Yankiel Yong',
    'website': '',
    'category': '',
    'depends': ['base', ],
    "data": [
        "security/ir.model.access.csv",
        "views/hotel.xml",
        "views/habitacion_views.xml",
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
