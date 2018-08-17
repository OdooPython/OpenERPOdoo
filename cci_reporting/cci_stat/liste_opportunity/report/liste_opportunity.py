# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
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
        if 'form' in data:
            # from_date = data['form']['date_aujourd']
            dateAuj = time.strftime('%d-%m-%Y %H:%M')
            ##############
            partner_id = data['form']['partner_id'][1]

            cash_ids = pool.get('res.partner').search(cr, uid, [('name', '=', partner_id)])
            cash_objs = pool.get('res.partner').browse(cr, uid, cash_ids)

            reg_ids = pool.get('crm.lead').search(cr, uid, [('partner_id', '=', cash_objs.id)])

            reg_objs = pool.get('crm.lead').browse(cr, uid, reg_ids)
            
            if reg_objs:

                for reg in reg_objs:
                    etape = reg.stage_id["name"]
                    if etape == 'New':
                        etape = 'Nouveau'
                    if etape == 'Dead':
                        etape = 'Perdu'
                    if etape == 'Qualification':
                        etape = 'Qualification'
                    if etape == 'Proposition':
                        etape = 'Proposition'
                    if etape == 'Negotiation':
                        etape = 'Negotiation'
                    if etape == 'Won':
                        etape = 'Gagné'
                    if etape == 'Lost':
                        etape = 'Perdu'

                    print ",,,,,,,",reg.section_id["name"]
                    section_id = pool.get('crm.lead').browse(cr, uid, reg.id).section_id.id
                    section_code = pool.get('crm.case.section').browse(cr, uid, section_id).code
                    print "........",section_code
                    data = {
                        'partner_id': reg.partner_id['name'],
                        'name': reg.product_id["name"],
                        'stage_id':etape,
                        'section_id':section_code,
                        'dateAuj': dateAuj,

                    }

                    result.append(data)

            else:
                data = {
                    'name': '',
                    'partner_id': '',
                    'product_id': '',
                    'stage_id': '',
                    'section_id': '',
                    'dateAuj': dateAuj,

                }
                result.append(data)
            ##############""

        return result


jasper_report.report_jasper('report.jasper_opportunity_print', 'crm.lead', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
