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
		revenue_total = 0
		total_participant = 0
		if 'form' in data:
			product_id = data['form']['product_id'][1]
			debut = data['form']['debut']
			fin = data['form']['fin']

			d_deb = datetime.datetime.strptime(debut, "%Y-%m-%d").strftime('%d-%m-%Y')
			d_fin = datetime.datetime.strptime(fin, "%Y-%m-%d").strftime('%d-%m-%Y')

			#id_prod = data['form']['product_id'][0]
			dateAuj = time.strftime('%d-%m-%Y %H:%M')

            # --------------------------Liste des secteurs d'activités
			#product = pool.get('product.template').search(cr, uid, [('name', '=', product_id)])
			#print "product.......",product
			#product_objs = pool.get('product.template').browse(cr, uid, product)
			#print "",product_objs
			#secteurs_ids =  pool.get('product.template').browse(cr, uid, product).product_sector_ids
			#if secteurs_ids:
			#	for secteur in secteurs_ids:
					
			#		print 'secteurs_ids.....................',secteur
			#		data = {
			#			'secteur_activity':secteur.id,
			#		}
			#		result.append(data)
			#else:
			#	data = {
			#			'secteur_activity':'',
			#	}
			#	result.append(data)

			# ----------------------------date de debut et date fin
			reg_ids = pool.get('product.template').search(cr, uid, [('name', '=', product_id),('date_debut', '>=', d_deb),('date_fin', '<=', d_fin)])
			reg_objs = pool.get('product.template').browse(cr, uid, reg_ids)

			# ----------------------------currency
			company_id = pool.get('res.company').search(cr,uid,[])
			currency_id = pool.get('res.company').browse(cr,uid,company_id).currency_id.id
			currency_name = pool.get('res.currency').browse(cr,uid,currency_id).name


			if reg_objs:

				for reg in reg_objs:
					
					date_debut_prod = datetime.datetime.strptime(reg.date_debut, "%Y-%m-%d").strftime('%d-%m-%Y')
					date_fin_prod = datetime.datetime.strptime(reg.date_fin, "%Y-%m-%d").strftime('%d-%m-%Y')

					category_id =  pool.get('product.template').browse(cr, uid, reg.id).categ_id.id

					categ_name = pool.get('product.category').browse(cr, uid, category_id).name
					planned_revenue =  pool.get('product.template').browse(cr, uid, reg.id).list_price

					
					data = {
						
						'date_debut': d_deb,
						'date_fin': d_fin,
						'prod_date_deb':date_debut_prod,
						'prod_date_fin':date_fin_prod,
						'planned_revenue':planned_revenue,
						'currency_name':currency_name,
						'category_id':categ_name,
						'product_id': product_id,
						'dateAuj': dateAuj,
					}
					result.append(data)

			else:
				
				data = {
					'date_debut': '',
					'date_fin': '',
					'prod_date_deb':'',
					'prod_date_fin':'',
					'planned_revenue':'',
					'currency_name':'',
					'product_id': product_id,
					'category_id':'',
					'dateAuj': dateAuj,
				}
				result.append(data)

			# -----------------------------liste des participants
			participant_ids = pool.get('participant.contact').search(cr, uid, [('product_id', '=', reg_objs.id)])
			participant_objs = pool.get('participant.contact').browse(cr, uid, participant_ids)
			total_participant = 0
			if participant_objs:
				for par in participant_objs:
					total_participant = total_participant + 1

					data = {
						'name': par.name["name"],
						'participant_id': par.participant_id["name"].name,
					}
					result.append(data)

			

		# 	# -----------------------------liste des présences
			presence_ids = pool.get('session.presence').search(cr, uid, [])
			presence_objs = pool.get('session.presence').browse(cr, uid, presence_ids)
			if presence_objs:

				for pre in presence_objs:
					contact_id = pre.contact_id
					session_id = pre.session_id

					cr.execute("SELECT * FROM participant_contact WHERE id =%s", (contact_id.id,))
					lines = cr.dictfetchall()
					for line in lines:
						name = line['name']

						cont = pool.get('res.partner').browse(cr, uid, name).name

						cr.execute("SELECT * FROM product_session WHERE id =%s", (session_id.id,))
						lines = cr.dictfetchall()
						for line in lines:
							id = line['id']

						session_name = pool.get('product.session').browse(cr, uid, id).name

						data = {
							'contact_id': cont,
							'session_id': session_name,
							'dateAuj': dateAuj,
						}

						result.append(data)
			else:
				data = {
					'dateAuj': dateAuj,
					'contact_id': '',
					'session_id': '',
				}
				result.append(data)

			# ------------------------revenue realisé
			crm_ids = pool.get('crm.lead').search(cr, uid, [('product_id', '=', reg_objs.id)])
			crm_objs = pool.get('crm.lead').browse(cr, uid, crm_ids)

			if crm_objs:
				for opp in crm_objs:
					if opp.stage_id.name == "Won":
						revenue_total = revenue_total + opp.planned_revenue
					data = {
						'revenue_total': revenue_total,
					}
					result.append(data)

			# -----------------------------liste des sessions-------------------------
			session_ids = pool.get('product.session').search(cr, uid, [('product_id', '=', reg_objs.id)])
			session_objs = pool.get('product.session').browse(cr, uid, session_ids)
			if session_objs:
				for session in session_objs:
					date_deb_ses = datetime.datetime.strptime(session.heure_debut, "%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y %H:%M')
					date_fin_ses = datetime.datetime.strptime(session.heure_fin, "%Y-%m-%d %H:%M:%S").strftime('%d-%m-%Y %H:%M')

					data = {
						'titre_ses': session.name,
						'date_deb_ses': date_deb_ses,
						'date_fin_ses': date_fin_ses,
					}
					result.append(data)



				# ---------------------liste des reclamations----------------------
			claim_ids = pool.get('crm.claim').search(cr, uid, [('product_id', '=', reg_objs.id)])
			claim_objs = pool.get('crm.claim').browse(cr, uid, claim_ids)

			if claim_objs:
				print 'claim_objs......',claim_objs
				for claim in claim_objs:
					data = {
						'objet': claim.name,
						'partner': claim.partner_id["name"],
						'date_reclamation': claim.date,
						'echeance': claim.date_deadline,
						'responsable': claim.user_id["name"],
						'state': claim.stage_id['name'],
					}
					result.append(data)

		# -----------------------------------

		data = {
			'revenue_total': repr(revenue_total),
			'total_participant': repr(total_participant),
		}
		result.append(data)

		return result


jasper_report.report_jasper('report.jasper_fiche_product_print', 'crm.lead', parser=jasper_client, )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:c
