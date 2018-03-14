# -*- coding: utf-8 -*-
{
    'name': 'Ticket de Entrada/Salida de Inventarios',
    'version': '1.2.0',
    'category': 'Castalia',
    'description': """
    Modulo que crea formatos para las operaciones de Entradas y Salidas de almacen.
    """,
    'author': 'Humanytek',
    'website': 'http://www.humanytek.com',
    'depends': [
        'stock',
        'purchase',
    ],
    'data': [
        'report/ticket.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
