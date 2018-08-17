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
            dateAuj = time.strftime('%d-%m-%Y %H:%M')
            date_debut = data['form']['date_debut']
            date_fin = data['form']['date_fin']
            partner_ids = data['form']['partner_ids']
            section_ids = data['form']['section_ids']
            user_ids = data['form']['user_ids']
            secteur_ids = data['form']['secteur_ids']
            operateur = data['form']['operateur']
            commercial = data['form']['commercial']
            print "...........",partner_ids,".",section_ids,".",user_ids,".",secteur_ids
            
            data = {
                'date_debut':date_debut,
                'date_fin':date_fin,
                'dateAuj': dateAuj,
                 }
            
            result.append(data)

            if operateur :
                print '........opérateur'
                for partner in partner_ids:
                    print '........opérateur',partner
                


            if commercial :
                print '........commercial'
                for user in user_ids:
                    print '........commercial',user

            
            data = {
                 }
            
            result.append(data)
        return result


jasper_report.report_jasper('report.jasper_options_print', 'crm.lead', parser=jasper_client, )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
