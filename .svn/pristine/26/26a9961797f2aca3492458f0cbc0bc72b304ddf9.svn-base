# encoding: utf-8
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
import datetime
from operator import itemgetter

# import base64
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
		total_mont_adh = 0
		total_mont_op = 0
		list_category = []
		list_categ_name = []
		pool = pooler.get_pool(cr.dbname)
		result = []
		if 'form' in data:
			dateAuj = time.strftime('%d-%m-%Y %H:%M')
			op_eco_id = data['form']['op_eco_id'][0]

			op_eco_obj = pool.get('res.partner').browse(cr, uid, op_eco_id)
			street = self.pool.get('res.partner').browse(cr, uid, op_eco_id).street
			street2 = self.pool.get('res.partner').browse(cr, uid, op_eco_id).street2
			city = self.pool.get('res.partner').browse(cr, uid, op_eco_id).city
			zip = self.pool.get('res.partner').browse(cr, uid, op_eco_id).zip

			country_id = self.pool.get('res.partner').browse(cr, uid, op_eco_id).country_id.id
			country= self.pool.get('res.country').browse(cr, uid, country_id).name
			


			cr.execute("SELECT category_id FROM res_partner_res_partner_category_rel WHERE partner_id =%s",(op_eco_id,))	
			lines = cr.dictfetchall()
			for line in lines:
				category_id = line['category_id']
				list_category.append(category_id)

			cr.execute('SELECT product_template_id FROM product_template_res_partner_category_rel WHERE res_partner_category_id in %s',(tuple(list_category),))
			lines_p = cr.dictfetchall()
			for product in lines_p:
				product_template_id = product['product_template_id']
			categ_id = self.pool.get('product.template').browse(cr, uid, product_template_id, context=context).categ_id.id

			cr.execute('SELECT crm_case_section_id FROM crm_case_section_product_category_rel WHERE product_category_id=%s',(categ_id,))
			lines_Dep = cr.dictfetchall()
			for line_dep in lines_Dep:
				section_id = line_dep['crm_case_section_id']

			section_code = self.pool.get('crm.case.section').browse(cr,uid,section_id,context=context).code
			section = self.pool.get('crm.case.section').browse(cr,uid,section_id,context=context).name



			for cat in list_category :
				category = self.pool.get('res.partner.category').browse(cr,uid,cat,context=context).name
				list_categ_name.append(category) 

				data = {
					'dateAuj': dateAuj,
					'nom_op_eco':op_eco_obj[0].name,
					'category':category,
					'street':street,
					'street2':street2,
					'city':city,
					'zip':zip,
					'country':country,
					'section':section,
					'section_code':section_code,
					'mont_op_lost':'',

				}
				result.append(data)

			ops_ids = pool.get('crm.lead').search(cr, uid, [('partner_id', '=', op_eco_id),('stage_id.name','=','Won')])
			ops_objs = pool.get('crm.lead').browse(cr, uid, ops_ids)

			if ops_objs:
				for op in ops_objs:
					total_mont_op = total_mont_op + op.planned_revenue
					data = {
						'date_op': datetime.datetime.strptime(op.date_debut,"%Y-%m-%d"),
						'nom_op': u'Participer à ' + op.name,
						'category':category,
						'street':street,
						'street2':street2,
						'city':city,
						'zip':zip,
						'country':country,
						'mont_op': repr(op.planned_revenue),
						'section':section,
						'section_code':section_code,
						'mont_op_lost':'',
					}
					result.append(data)
			#adh_ids = pool.get('membership.membership_line').search(cr, uid, [('partner', '=', op_eco_id)])
			#adh_lines_objs = pool.get('membership.membership_line').browse(cr, uid, adh_ids)
			#if adh_lines_objs:
			#	for adh in adh_lines_objs:
			#		adh_obj = pool.get('product.product').browse(cr, uid, adh.membership_id.id)
					#adh_date = time.strptime(adh.write_date)
			#		total_mont_adh = total_mont_adh + adh.member_price
			#		data = {
			#			'date_op':datetime.datetime.strptime(adh.write_date,"%Y-%m-%d %H:%M:%S"),
			#			'nom_op' : u'Adhésion ' + adh_obj.name_template,
			#			'mont_op':repr(adh.member_price),
			#		}
			#		result.append(data)

			
		#-----------------Sort operations by date--------------------
		print "...............res",result[0:]
		# is equivalent to a shallow copied list of all elements starting from the 0-indexed 1
		rows_by_date_op = sorted(result[2:], key=itemgetter('date_op'))

		for obj in rows_by_date_op:
			if 'date_op' in obj:
				obj['date_op'] = datetime.datetime.strftime(obj['date_op'], "%d-%m-%Y")


		rows_by_date_op.insert(0,result[0])

		return rows_by_date_op
		
jasper_report.report_jasper('report.jasper_fiche_op_eco_print', 'res.partner', parser=jasper_client, )
