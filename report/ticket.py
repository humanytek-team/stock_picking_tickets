# -*- coding: utf-8 -*-
# Copyright 2018 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import api, models

from .. import amount_to_text_es_MX


class TicketReport(models.AbstractModel):
    _name = 'report.stock_picking_tickets.template_inv_ticket'

    @api.multi
    def render_html(self, data):

        docids = self.ids
        Report = self.env['report']
        report = Report._get_report_from_name(
            'stock_picking_tickets.template_inv_ticket')
        StockPicking = self.env['stock.picking']
        docs = StockPicking.browse(docids)

        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docs,
            'get_total_line': self.get_total_line,
            'get_total': self.get_total,
            'get_price_by_sale': self.get_price_by_sale,
            'get_price_by_purchase': self.get_price_by_purchase,
            'amount_to_text': self.amount_to_text,
        }

        return Report.render(
            'stock_picking_tickets.template_inv_ticket', docargs)

    @api.model
    def get_price_by_sale(self, sale, product):
        sale_id = self.env['sale.order'].search(
            [('name', '=', sale)], limit=1).id
        return self.env['sale.order.line'].search([('order_id', '=', sale_id), ('product_id', '=', product.id)]).price_unit

    @api.model
    def get_price_by_purchase(self, purchase, product):
        purchase_id = self.env['purchase.order'].search(
            [('name', '=', purchase)], limit=1).id
        return self.env['purchase.order.line'].search([('order_id', '=', purchase_id), ('product_id', '=', product.id)]).price_unit

    @api.model
    def get_total_line(self, product_qty, product_price, product_taxes=False):
        """Calculate total price with taxes of products processed."""
        total = product_qty * product_price

        if product_taxes:
            for tax in product_taxes:

                total += total * tax.amount / 100

        return total

    @api.model
    def get_total(self, picking, taxes=False, tax_total=False):
        total = 0
        total_tax = 0
        if picking.picking_type_code == 'outgoing':
            for move in picking.move_lines:
                if move.state == 'done' and move.product_uom_qty > 0:
                    total_line = move.product_uom_qty * move.procurement_id.sale_line_id.price_unit
                    total += total_line
                    if taxes:
                        for tax in move.procurement_id.sale_line_id.tax_id:
                            total += total_line * tax.amount / 100
                            if tax_total:
                                total_tax += total_line * tax.amount / 100
        elif picking.picking_type_code == 'incoming':
            for move in picking.move_lines:
                if move.state == 'done' and move.product_uom_qty > 0:
                    total_line = move.product_uom_qty * move.purchase_line_id.price_unit
                    total += total_line
                    if taxes:
                        for tax in move.purchase_line_id.taxes_id:
                            total += total_line * tax.amount / 100
                            if tax_total:
                                total_tax += total_line * tax.amount / 100
        if tax_total:
            return total_tax
        return total

    @api.multi
    def amount_to_text(self, total, currency):

        text_total = amount_to_text_es_MX.get_amount_to_text(
            self, float(total), currency)

        return text_total
