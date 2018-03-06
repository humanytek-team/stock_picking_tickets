# -*- coding: utf-8 -*-
{
    'name': 'Ticket de Entrada/Salida de Inventarios',
    'version': '1.1',
    'category': 'Castalia',
    'description': """
    Modulo que crea formatos para las operaciones de Entradas y Salidas de almacen.
    """,
    'author': 'Humanytek',
    'website': 'http://www.humanytek.com',
    'depends': [
        'stock',
        'purchase',
        'stock_sale_order_line',
    ],
    'data': [
        'report/ticket.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
