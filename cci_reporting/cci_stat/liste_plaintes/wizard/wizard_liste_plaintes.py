# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class wizard_claim(osv.osv_memory):
    _name = "cci.wizard.claim"
    _description = "Claim Wizard"

    _columns = {
        'product_id': fields.many2one('product.template', 'Produit', required=True),

    }


    def create_report(self, cr, uid, ids, context=None):
        datas = {}
        if context is None:
            context = {}
        data = self.read(cr, uid, ids)[0]
        datas = {
            'ids': [],
            'model': 'object.object',
            'form': data
        }
        return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_claim_print', 'datas': datas}

wizard_claim()
