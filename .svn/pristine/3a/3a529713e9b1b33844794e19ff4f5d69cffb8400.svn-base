# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from datetime import date
import time



class crm_lead(osv.Model):
	_inherit = "crm.lead"
	# _rec_name = "product_id"
	_columns = {
		'name': fields.char(required=False),
		'product_id': fields.many2one('product.template', string="Produit", required=True),
		'date_debut': fields.date("Date de declanchement", readonly=True, default=date.today()),
		'date_fin':fields.date("Date de clôture",readonly=True),
		'date_deadline':fields.datetime(),

	}


	def onchange_revenue(self, cr, uid, ids, product_id, context=None):
		price = self.pool.get('product.template').browse(cr, uid, product_id, context=context).list_price
		return {'value': {'planned_revenue': price}}

	def case_mark_won(self, cr, uid, ids, context=None):
		""" Mark the case as won: state=done and probability=100
		"""
		res = super(crm_lead, self).case_mark_won(cr, uid, ids, context)

		#--------------création des opérateurs dans l'article 14-09-2017
		opprtunity_id=self.browse(cr, uid, ids, context=context).id

		product_idd = self.browse(cr, uid, opprtunity_id, context=context).product_id.id

		res_partner = self.browse(cr, uid, opprtunity_id, context=context).partner_id.id
		obj = self.pool.get('product.participant')
		partner_product_ids = self.pool.get('product.participant').search(cr, uid, [('product_id', '=', product_idd),('name', '=', res_partner)],context=context)

		if len(partner_product_ids) == 0:
			val = {
				'name': res_partner,
				'product_id':product_idd,
			}
			inv_id = self.pool.get('product.participant').create(cr, uid, val)
		#--------------ajout la date de cloture
		active_record = self.browse(cr, uid, ids[0], context=context)
		active_record.date_fin = time.strftime('%Y-%m-%d')
		return res

	def case_mark_lost(self, cr, uid, ids, context=None):
		super(crm_lead, self).case_mark_lost(cr, uid, ids, context)
		active_record = self.browse(cr, uid, ids[0], context=context)
		active_record.date_fin = time.strftime('%Y-%m-%d')



	def create(self, cr, uid, vals, context=None):
		prod_name = self.pool.get('product.template').browse(cr, uid, vals['product_id'], context=context).name
		vals['name'] = prod_name
		print "....create crm lead .......",vals
		type_act = vals.get('type_act')
		date_act = vals.get('date_action')
		date_deadline = vals.get('date_deadline')
		title_act = vals.get('title_action')
		if type_act:
			if type_act == 'Mail': 
				type_name = "Email"
			if type_act == 'Appel':
				type_name = "Appel"
			if type_act == 'Reunion':
				type_name = "Réunion"

			calendar_vals = {

					'start_datetime':date_act,
					'name':type_name+': '+title_act,
					'user_id': uid,
					'stop':date_deadline,


					}
			print "calendar_vals ......",calendar_vals
			calendar = self.pool.get('calendar.event').create(cr, uid, calendar_vals)
		return super(crm_lead, self).create(cr, uid, vals, context=None)



	#wheN the stage_id change to won the operator add into the product
    	def write(self, cr, uid, ids, vals, context=None):
		print "whe the stage_id change to won the operator add into the product...."
		stage_id = vals.get('stage_id')

		opprtunity_id = self.browse(cr, uid, ids, context=context).id
		product_id = self.browse(cr, uid, opprtunity_id, context=context).product_id.id
		res_partner = self.browse(cr, uid, opprtunity_id, context=context).partner_id.id
		obj = self.pool.get('product.participant')
		type_act = vals.get('type_act')
		date_act = vals.get('date_action')
		date_deadline = vals.get('date_deadline')
		title_act = vals.get('title_action')


		if stage_id == 6:
			val = {
				'name': res_partner,
				'product_id':product_id,
			}

			res = obj.search(cr,uid, [('name','=',res_partner),('product_id','=',product_id)],context=context)
			if not res :
				obj.create(cr, uid, val)
				self.write(cr, uid, ids,{'date_fin':time.strftime('%Y-%m-%d')}, context=context)
			else :
				date_fin = time.strftime('%Y-%m-%d')
				self.write(cr, uid, ids,{'date_fin':time.strftime('%Y-%m-%d')}, context=context)

		if stage_id in {1,2,3,4,5}:
			unlink = cr.execute ("DELETE FROM product_participant WHERE name=%s AND product_id=%s",(res_partner,product_id))
			self.write(cr, uid, ids,{'date_fin':False}, context=context)

		if stage_id == 7:
			unlink = cr.execute ("DELETE FROM product_participant WHERE name=%s AND product_id=%s",(res_partner,product_id))
			obj.unlink(cr, uid, ids, context=context)
			self.write(cr, uid, ids,{'date_fin':time.strftime('%Y-%m-%d')}, context=context)
		if type_act:
			if type_act == 'Mail': 
				type_name = "Email"
			if type_act == 'Appel':
				type_name = "Appel"
			if type_act == 'Reunion':
				type_name = "Réunion"


			calendar_vals = {

					'start_datetime':date_act,
					'name':type_name+': '+title_act,
					'user_id': uid,
					'stop':date_deadline,


					}
			print "calendar_vals ......",calendar_vals
			calendar = self.pool.get('calendar.event').create(cr, uid, calendar_vals)

		return super(crm_lead, self).write(cr, uid, ids, vals, context=context)
		

        	 

