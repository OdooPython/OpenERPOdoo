# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime,date

class wizard_performance(osv.osv_memory):
    _name = "cci.wizard.fiche.op.eco"

    _columns = {
        'op_eco_id':fields.many2one('res.partner',required=True,domain="[('is_company', '=', True)]")
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
        return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_fiche_op_eco_print', 'datas': datas}


wizard_performance()

