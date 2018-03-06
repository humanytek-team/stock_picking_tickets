# -*- coding: utf-8 -*-
from openerp import addons
from openerp import models, fields, api, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError
#from dateutil.relativedelta import relativedelta
#from datetime import timedelta
from datetime import datetime, timedelta, date
import time
import amount_to_text_es_MX

class stock_picking(models.Model):
    _inherit = ['stock.picking']        

    @api.multi
    def check_vat_mx(self, vat):
        # we convert to 8-bit encoding, to help the regex parse only bytes
        vatt = vat.replace('MX','')
       
        return vatt
  
    @api.multi
    def calculate_sp_total(self, pack_operation_product_ids, type):
        #print "##### calculate_sp_total"
        total = 0.0
        if not pack_operation_product_ids:
            return total

        for line in pack_operation_product_ids:
            if line.qty_done>0:
                if type == 'incoming':
                    total += line.qty_done * line.product_id.standard_price
                else:
                    total += line.qty_done * line.product_id.lst_price

        return total

    @api.multi
    def calculate_sp_total_qty(self, pack_operation_product_ids):
        #print "##### calculate_sp_total"
        total = 0
        if not pack_operation_product_ids:
            return total

        for line in pack_operation_product_ids:
            if line.qty_done>0:
                total += line.qty_done

        return total

    @api.multi
    def amount_to_text(self, pack_operation_product_ids, type):
        #print "##### calculate_sp_total"
        text_total = ''
        total= 0.0
        moneda = self.company_id.currency_id.name
        if not pack_operation_product_ids:
            return text_total

        for line in pack_operation_product_ids:
            if line.qty_done>0:
                if type == 'incoming':
                    total += (line.qty_done * line.product_id.standard_price) *1.16
                else:
                    total += (line.qty_done * line.product_id.lst_price) *1.16


        text_total = amount_to_text_es_MX.get_amount_to_text(self,float(total),moneda)
        #rec.amount_to_text = amount_to_text_es_MX.get_amount_to_text(rec,rec.amount_total, rec.currency_id.name)

        return text_total
 
