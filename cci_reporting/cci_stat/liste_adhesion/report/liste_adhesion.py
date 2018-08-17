# -*- encoding: utf-8 -*-
import JasperDataParser
from openerp.jasper_reports import jasper_report
from openerp import pooler
import time
from datetime import datetime
import base64
import os
# import netsvc
from openerp.osv import fields, osv
from openerp.tools.translate import _

import datetime


class jasper_client(JasperDataParser.JasperDataParser):
    def __init__(self, cr, uid, ids, data, context):
        super(jasper_client, self).__init__(cr, uid, ids, data, context)

    def generate_data_source(self, cr, uid, ids, data, context):
        return 'records'

    def generate_parameters(self, cr, uid, ids, data, context):
        return {}

    def generate_properties(self, cr, uid, ids, data, context):
        return {}

    def generate_records(self, cr, uid, ids, data, context):
        pool = pooler.get_pool(cr.dbname)
        result = []
        total_mont_adh = 0
        if 'form' in data:
            op_eco_id = data['form']['op_eco_id'][0]
            op_eco_obj = pool.get('res.partner').browse(cr, uid, op_eco_id)

            adh_ids = pool.get('membership.membership_line').search(cr, uid, [('partner', '=', op_eco_id)])

            adh_lines_objs = pool.get('membership.membership_line').browse(cr, uid, adh_ids)

            data = {
				'nom_op_eco':op_eco_obj[0].name,
			}

            result.append(data)

            #if adh_lines_objs:
            if adh_lines_objs:
                for adh in adh_lines_objs:
                    adh_obj = pool.get('product.product').browse(cr, uid, adh.membership_id.id)
                    #adh_date = time.strptime(adh.write_date)
                    total_mont_adh = total_mont_adh + adh.member_price
                    data = {
					    'date_op':datetime.datetime.strptime(adh.write_date,"%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y'),
					    'nom_op' :adh_obj.name_template,
					    'mont_op':repr(adh.member_price), 
				    }
                    result.append(data)

        return result



jasper_report.report_jasper('report.jasper_adhesion_print', 'res.partner', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
