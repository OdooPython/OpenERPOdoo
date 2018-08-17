# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime
from random import *
from itertools import cycle


class wizard_product(osv.osv_memory):
	_name = "wizard.product"
	_description = "lancer Compagne Marketing"

	_columns = {
		'product_id': fields.many2one('product.template', "Produit"),
		'partner_list': fields.one2many('res.partner', 'id', string='op'),
	}

	def get_operateur(self, cr, uid, ids, context=None):
		list_members = []
		list_partners = []
		list_category=[]

		product_wi_id = self.browse(cr, uid, ids, context=context)[0].id

		product_tmp_id = self.browse(cr, uid, product_wi_id, context=context).product_id.id

		product_price = self.pool.get('product.template').browse(cr, uid, product_tmp_id, context=context).list_price

		cr.execute(
			'SELECT res_partner_category_id FROM product_template_res_partner_category_rel WHERE product_template_id=%s',(product_tmp_id,))
		lines_partner = cr.dictfetchall()

		for line_partner in lines_partner:
			res_partner_category_id = line_partner['res_partner_category_id']
		 	list_category.append(res_partner_category_id)

		#add 19-10-2017 by marwa
		list_category=tuple(list_category)


		# cursor.execute('SELECT * FROM table where id in %(list_category)s', params)
		# for category in list_category:
		# 	category_id =
		# placeholder = '?'  # For SQLite. See DBAPI paramstyle.
		# placeholders = ', '.join(placeholder for unused in list_category)
		# print '......placeholders',placeholders
		cr.execute('SELECT partner_id FROM res_partner_res_partner_category_rel WHERE category_id IN %s',(list_category,))
		lines = cr.dictfetchall()

		# Update by marwa 11-09-2017
		for line in lines:
			partner_id = line['partner_id']
			cr.execute('SELECT id,phone,email FROM res_partner WHERE id=%s AND is_company =%s', (partner_id, True))
			partner_lines = cr.dictfetchall()


			for i in partner_lines:
				id_partner = i['id']
				phone = i['phone']
				email= i['email']
				list_partners.append(id_partner)

		print '........list_partners',list_partners
		#compare and delete occurence 19-10-2017
		for id in list_partners :
			count=list_partners.count(id)
			if count > 1:
				list_partners.remove(id)

		categ_id = self.pool.get('product.template').browse(cr, uid, product_tmp_id, context=context).categ_id.id
		print 'categ_id .....',categ_id
		cr.execute('SELECT crm_case_section_id FROM crm_case_section_product_category_rel WHERE product_category_id=%s',(categ_id,))
		lines_Dep = cr.dictfetchall()
		for line_dep in lines_Dep:
			crm_case_section_id = line_dep['crm_case_section_id']

			cr.execute('SELECT member_id FROM sale_member_rel WHERE section_id=%s', (crm_case_section_id,))
			lines_member = cr.dictfetchall()

			for line_member in lines_member:
				member_id = line_member['member_id']
				list_members.append(member_id)

		# ---------------------------add by Houssem-------------------------------------

		crm_lead = self.pool.get('crm.lead')
		j = 0
		for i in range(max((len(list_members), len(list_partners)))):
			try:
				#récupération du département du membre
				cr.execute('SELECT section_id FROM sale_member_rel WHERE member_id=%s', (list_members[i],))
				section_id = cr.fetchall()
				vals = {
					'partner_id': list_partners[i],
					'type': 'opportunity',
					'user_id': list_members[i],
					'phone':phone,
					'email_from':email,
					'product_id': product_tmp_id,
					'section_id': section_id[0][0],
					'planned_revenue': product_price,
				}
				crm_lead.create(cr,uid,vals)
			except IndexError:
				if len(list_partners) > len(list_members):

					# si la liste des membres (list_members) est términée, recommencer l'iteration sur cette liste pour
					# affecter les opérateurs économiques pour les opérateurs économiques (list_partners) restants
					restart = True
					while j < len(list_members) and restart:
						cr.execute('SELECT section_id FROM sale_member_rel WHERE member_id=%s', (list_members[j],))
						section_id = cr.fetchall()
						vals = {
							'partner_id': list_partners[i],
							'type': 'opportunity',
							'user_id': list_members[j],
							'product_id': product_tmp_id,
							'section_id': section_id[0][0],
							'planned_revenue': product_price,
						}

						crm_lead.create(cr, uid, vals)

						# arreter la boucle sur la liste des membres (list_members) si la liste
						# des opérateurs économiques (list_partners) est terminée
						if i == len(list_partners) - 1:
							restart = False

						# recommencer la boucle si la fin de la liste des membres (list_members) est atteinte
						if j == len(list_members) - 1:
							j = 0

						# changer à chaque éxécution de la boucle, l'indice de l'itération,
						# pour pointer à chaque fois sur un membre
						else:
							j = j + 1

						# exécuter toujours une seule itération
						break
				elif len(list_partners) < len(list_members):
					break

		return True
