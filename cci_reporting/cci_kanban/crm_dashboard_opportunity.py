#-*- coding:utf-8 -*-
import json
import time
from datetime import date, datetime, timedelta
import calendar
from babel.dates import format_datetime, format_date
from openerp import models, api, _, fields
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class crm_dashboard_opportunity(models.Model):
    _name = "crm.dashboard.opportunity"

    @api.one
    def _kanban_dashboard(self):
        self.kanban_dashboard = json.dumps(self.get_journal_dashboard_datas())



    @api.one
    def _dashboard_opportunity_state(self):
		self.dashboard_opportunity_state = json.dumps(self.get_dashboard_opportunity_state())
    @api.one
    def _dashboard_opportunity_dep(self):
		self.dashboard_opportunity_dep = json.dumps(self.get_dashboard_opportunity_dep())
    @api.one
    def _dashboard_opportunity_ag(self):
		self.dashboard_opportunity_ag = json.dumps(self.get_dashboard_opportunity_ag())

    @api.one
    def _dashboard_change_opportunity_won(self):
		self.dashboard_change_opportunity_won = json.dumps(self.get_dashboard_change_opportunity_won())
    @api.one
    def _dashboard_change_opportunity_lost(self):
		self.dashboard_change_opportunity_lost = json.dumps(self.get_dashboard_change_opportunity_lost())
    @api.one
    def _dashboard_change_opportunity_won_dep(self):
		self.dashboard_change_opportunity_won_dep = json.dumps(self.get_dashboard_change_opportunity_won_dep())
    @api.one
    def _dashboard_change_opportunity_lost_dep(self):
		self.dashboard_change_opportunity_lost_dep = json.dumps(self.get_dashboard_change_opportunity_lost_dep())
    @api.one
    def _dashboard_vision_state(self):
		self.dashboard_vision_state = json.dumps(self.get_dashboard_vision_state())
    @api.one
    def _dashboard_vision_dep(self):
		self.dashboard_vision_dep = json.dumps(self.get_dashboard_vision_dep())
    @api.one
    def _dashboard_vision_ag(self):
		self.dashboard_vision_ag = json.dumps(self.get_dashboard_vision_ag())
    @api.one
    def _dashboard_ca_ag(self):
		self.dashboard_ca_ag = json.dumps(self.get_dashboard_ca_ag())
    @api.one
    def _dashboard_ca_dep(self):
		self.dashboard_ca_dep = json.dumps(self.get_dashboard_ca_dep())
    @api.one
    def _dashboard_top_ten(self):
		self.dashboard_top_ten = json.dumps(self.get_dashboard_top_ten())
    @api.one
    def _dashboard_change_opportunity_won_period(self):
		self.dashboard_change_opportunity_won_period = json.dumps(self.get_dashboard_change_opportunity_won_period())
    @api.one
    def _dashboard_change_opportunity_lost_period(self):
		self.dashboard_change_opportunity_lost_period = json.dumps(self.get_dashboard_change_opportunity_lost_period())
    @api.one
    def _dashboard_change_opportunity_won_dep_period(self):
		self.dashboard_change_opportunity_won_dep_period = json.dumps(self.get_dashboard_change_opportunity_won_dep_period())
    @api.one
    def _dashboard_change_opportunity_lost_dep_period(self):
		self.dashboard_change_opportunity_lost_dep_period = json.dumps(self.get_dashboard_change_opportunity_lost_dep_period())

    @api.one
    def _dashboard_top_ten_revenue(self):
		self.dashboard_top_ten_revenue = json.dumps(self.get_dashboard_top_ten_revenue())



    name = fields.Char(string='Name') 
    type_dash = fields.Selection([('state', "state"),('ag', "ag"),('dep', "dep"),('op_dep_won', "op_dep_won"),('op_dep_lost', "op_dep_lost"),('opportunity_won', "opportunity_won"),('opportunity_lost', "opportunity_lost"),('vision_state', "vision_state"),('vision_dep', "vision_dep"),('vision_ag', "vision_ag"),('chiffre','chiffre'),('ca_dep','ca_dep'),('operateur','operateur'),('operateur_revenue',"operateur_revenue"),('op_won', "op_won"),('op_lost', "op_lost"),('period_won', "period_won"),('period_lost', "period_lost")]) 

    kanban_dashboard = fields.Text(compute='_kanban_dashboard')

    dashboard_opportunity_state = fields.Text(compute='_dashboard_opportunity_state')
    dashboard_opportunity_dep = fields.Text(compute='_dashboard_opportunity_dep')
    dashboard_opportunity_ag = fields.Text(compute='_dashboard_opportunity_ag')

    dashboard_change_opportunity_won = fields.Text(compute='_dashboard_change_opportunity_won')
    dashboard_change_opportunity_lost = fields.Text(compute='_dashboard_change_opportunity_lost')
    dashboard_change_opportunity_won_dep = fields.Text(compute='_dashboard_change_opportunity_won_dep')
    dashboard_change_opportunity_lost_dep = fields.Text(compute='_dashboard_change_opportunity_lost_dep')

    dashboard_vision_state = fields.Text(compute='_dashboard_vision_state')
    dashboard_vision_dep = fields.Text(compute='_dashboard_vision_dep')
    dashboard_vision_ag = fields.Text(compute='_dashboard_vision_ag')
    dashboard_ca_ag = fields.Text(compute='_dashboard_ca_ag')
    dashboard_ca_dep = fields.Text(compute='_dashboard_ca_dep')
    dashboard_top_ten = fields.Text(compute='_dashboard_top_ten')
    dashboard_top_ten_revenue = fields.Text(compute='_dashboard_top_ten_revenue')

    dashboard_change_opportunity_won_period = fields.Text(compute='_dashboard_change_opportunity_won_period')
    dashboard_change_opportunity_lost_period = fields.Text(compute='_dashboard_change_opportunity_lost_period')
    dashboard_change_opportunity_won_dep_period = fields.Text(compute='_dashboard_change_opportunity_won_dep_period')
    dashboard_change_opportunity_lost_dep_period = fields.Text(compute='_dashboard_change_opportunity_lost_dep_period')



    show_on_dashboard = fields.Boolean(string='Show journal on dashboard', help="Whether this journal should be displayed on the dashboard or not", default=True)


    @api.multi
    def get_journal_dashboard_datas(self):
	print "u call get_journal_dashboard_datas"

    ######################AVANT VENTE Nombre des opportunités par état ou à suivre est true (sauf gagné et perdu)
    @api.multi
    def get_dashboard_opportunity_state(self):
	data = []
	list_prod = []
	list_section = []
	value = 0
 	if self.type_dash == 'state' :
		user_id = self.env['res.users'].browse(self.env.uid).id
		print '....user_id...',user_id
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		print '....département...',section_ids
		if user_id == 1 : #pour l'administrateur
			
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
			if list_prod :
				self.env.cr.execute("SELECT COUNT(id), stage_id FROM crm_lead WHERE product_id in %s AND stage_id NOT IN %s GROUP BY stage_id",(tuple(list_prod),(6,7)))
				res = self.env.cr.dictfetchall()
				for i in res:
					stage_id = i['stage_id']

					value = i.get('count')
					state = self.env['crm.case.stage'].browse(stage_id).name
					data.append({'label':state , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

		elif section_ids :  #pour le chef du département
			
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)

			for section in section_ids:
				print "...dep..",section
				list_section.append(section.id)
			if list_prod :
				self.env.cr.execute("SELECT COUNT(id), stage_id FROM crm_lead WHERE product_id in %s AND section_id in %s AND stage_id NOT IN %s GROUP BY stage_id",(tuple(list_prod),tuple(list_section),(6,7)))
				res = self.env.cr.dictfetchall()
				for i in res:
					stage_id = i['stage_id']
					value = i.get('count')
					state = self.env['crm.case.stage'].browse(stage_id).name
					data.append({'label':state , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

		else : #pour le commercial 
			
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
			if list_prod :
				self.env.cr.execute("SELECT COUNT(id), stage_id, product_id FROM crm_lead WHERE product_id in %s AND user_id =%s AND stage_id NOT IN %s GROUP BY stage_id, product_id",(tuple(list_prod),user_id,(6,7)))
				res = self.env.cr.dictfetchall()
				for i in res:
					stage_id = i['stage_id']
					value = i.get('count')
					state = self.env['crm.case.stage'].browse(stage_id).name
					data.append({'label':state , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]



    ##################### AVANT VENTE Nombre des opportunités par département ou à suivre est true (sauf gagné et perdu)
    @api.multi
    def get_dashboard_opportunity_dep(self):
	data = []
	list_prod = []
	list_section = []
	value = 0
 	if self.type_dash == 'dep' :
		user_id = self.env['res.users'].browse(self.env.uid).id
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		if user_id == 1 : #pour l'administrateur
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
			if list_prod :
				self.env.cr.execute("SELECT COUNT(id), section_id FROM crm_lead WHERE product_id in %s AND stage_id NOT IN %s GROUP BY section_id ",(tuple(list_prod),(6,7)))
				res = self.env.cr.dictfetchall()
				for i in res:
					section_id = i['section_id']
					value = i.get('count')
					section = self.env['crm.case.section'].browse(section_id).name
					data.append({'label':section , 'value':value,'id':self.id})

				return [{'values': data, 'area': True,'id': self.id}]

		elif section_ids :  #pour le chef du département
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
			
			for section in section_ids:
				list_section.append(section.id)

			if list_prod :
				self.env.cr.execute("SELECT COUNT(id), section_id FROM crm_lead WHERE product_id in %s AND section_id in %s AND stage_id NOT IN %s GROUP BY section_id",(tuple(list_prod),tuple(list_section),(6,7)))
				res = self.env.cr.dictfetchall()
				for i in res:
					section_id = i['section_id']
					value = i.get('count')
					section = self.env['crm.case.section'].browse(section_id).name
					data.append({'label':section , 'value':value,'id':self.id})

				return [{'values': data, 'area': True,'id': self.id}]

		else : #pour le commercial
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)

			section_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
			for section in section_ids:
				list_section.append(section.id)

			if list_prod :
				self.env.cr.execute("SELECT COUNT(id), section_id FROM crm_lead WHERE product_id in %s AND section_id in %s GROUP BY section_id",(tuple(list_prod),tuple(list_section),))
				res = self.env.cr.dictfetchall()
				for i in res:
					section_id = i['section_id']
					value = i.get('count')
					section = self.env['crm.case.section'].browse(section_id).name
					data.append({'label':section , 'value':value,'id':self.id})

				return [{'values': data, 'area': True,'id': self.id}]

    ############## AVANT VENTE Nombre des opportunités par agent commercial ou à suivre est true
    @api.multi
    def get_dashboard_opportunity_ag(self):
	data = []
	list_prod = []
	list_section = []
	value = 0
 	if self.type_dash == 'ag' :
		user_id = self.env['res.users'].browse(self.env.uid).id
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		if user_id == 1 : #pour l'administrateur
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
			if list_prod:
				self.env.cr.execute("SELECT COUNT(id), user_id FROM crm_lead WHERE product_id in %s AND stage_id NOT IN %s GROUP BY user_id",(tuple(list_prod),(6,7)))
				res = self.env.cr.dictfetchall()
				for i in res:
					user_id = i['user_id']
					value = i.get('count')
					user = self.env['res.users'].browse(user_id).name
					data.append({'label':user , 'value':value,'id':self.id})

				return [{'values': data, 'area': True,'id': self.id}]

		elif section_ids :  #pour le chef du département
			print 'chef ...................'
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)

			for section in section_ids:
				print "...dep..",section
				list_section.append(section.id)
			if list_prod :
				self.env.cr.execute("SELECT COUNT(id), user_id FROM crm_lead WHERE product_id in %s AND section_id in %s AND stage_id NOT IN %s GROUP BY user_id ",(tuple(list_prod),tuple(list_section),(6,7)))
				res = self.env.cr.dictfetchall()
				for i in res:
					user_id = i['user_id']
					value = i.get('count')
					user = self.env['res.users'].browse(user_id).name
					data.append({'label':user , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

		else : #pour le commercial
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
			if list_prod :
				self.env.cr.execute("SELECT COUNT(id), user_id, product_id FROM crm_lead WHERE product_id in %s AND user_id =%s  AND stage_id NOT IN %s GROUP BY user_id, product_id",(tuple(list_prod),user_id,(6,7)))
				res = self.env.cr.dictfetchall()
				for i in res:
					user_id = i['user_id']
					value = i.get('count')
					user = self.env['res.users'].browse(user_id).name
					data.append({'label':user , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]


    #######################APRÈS VENTE"""""Nombre d'opportunité gagné par commercial
    @api.multi
    def get_dashboard_change_opportunity_won(self):
	data = []
	list_prod = []
	list_section = []
 	if self.type_dash == 'opportunity_won' :
		##Liste des produits à suivre
		user_id = self.env['res.users'].browse(self.env.uid).id
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		if user_id == 1 : #pour l'administrateur
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
			if list_prod :
				self.env.cr.execute("SELECT COUNT(id), user_id FROM crm_lead WHERE stage_id=%s AND product_id in %s GROUP BY user_id",(6,tuple(list_prod)))
				res = self.env.cr.dictfetchall()
				for opportunity in res :
					values_won = opportunity.get('count')
					user = opportunity.get('user_id')
					user_name = self.env['res.users'].browse(user).name
					data.append({'label':user_name, 'value':values_won,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

		elif section_ids: #pour le chef du département
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
			for section in section_ids:
				list_section.append(section.id)
			if list_prod :
				self.env.cr.execute("SELECT COUNT(id), user_id FROM crm_lead WHERE stage_id=%s AND product_id in %s AND section_id in %s GROUP BY user_id",(6,tuple(list_prod),tuple(list_section)))
				res = self.env.cr.dictfetchall()
				for opportunity in res :
					values_won = opportunity.get('count')
					user = opportunity.get('user_id')
					user_name = self.env['res.users'].browse(user).name
					data.append({'label':user_name, 'value':values_won,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]
		else : #pour le commercial
			section_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
			if list_prod :
				self.env.cr.execute("SELECT COUNT(id), user_id FROM crm_lead WHERE user_id =%s AND stage_id=%s AND product_id in %s GROUP BY user_id",(user_id,6,tuple(list_prod)))
				res = self.env.cr.dictfetchall()
				for opportunity in res :
					values_won = opportunity.get('count')
					user = opportunity.get('user_id')
					user_name = self.env['res.users'].browse(user).name
					data.append({'label':user_name, 'value':values_won,'id':self.id})

				return [{'values': data, 'area': True,'id': self.id}]

    #######################APRÈS VENTE"""""Nombre d'opportunité perdu par commercial
    @api.multi
    def get_dashboard_change_opportunity_lost(self):
	data = []
	list_prod = []
	list_section =[]
 	if self.type_dash == 'opportunity_lost' :
		###utilisateur en cours"
		user_id = self.env['res.users'].browse(self.env.uid).id
	
		##Liste des produits à suivre
		product_ids = self.env['product.template'].search([('a_suivre','=',True)])
		for product in product_ids :
			list_prod.append(product.id)

		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		if user_id == 1 : #pour l'administrateur
			if list_prod :
				self.env.cr.execute("SELECT COUNT(id), user_id FROM crm_lead WHERE stage_id=%s AND product_id in %s GROUP BY user_id",(7,tuple(list_prod)))
				res = self.env.cr.dictfetchall()
				for opportunity in res :
					values_lost = opportunity.get('count')
					user = opportunity.get('user_id')
					user_name = self.env['res.users'].browse(user).name

					data.append({'label':user_name, 'value':values_lost,'id':self.id})
				return [{'values': data, 'area': True}]

		elif section_ids: #pour le chef du département
			for section in section_ids:
				list_section.append(section.id)
			if list_prod :
				self.env.cr.execute("SELECT COUNT(id), user_id FROM crm_lead WHERE stage_id=%s AND product_id in %s AND section_id in %s GROUP BY user_id",(7,tuple(list_prod),tuple(list_section)))
				res = self.env.cr.dictfetchall()
				for opportunity in res :
					values_lost = opportunity.get('count')
					user = opportunity.get('user_id')
					user_name = self.env['res.users'].browse(user).name
					data.append({'label':user_name, 'value':values_lost,'id':self.id})
				return [{'values': data, 'area': True}]
			
		else : #pour le commercial
			section_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
			for section in section_ids:
				list_section.append(section.id)
			if list_prod :
				self.env.cr.execute("SELECT COUNT(id), user_id FROM crm_lead WHERE stage_id=%s AND product_id in %s AND section_id in %s AND user_id=%s GROUP BY user_id",(7,tuple(list_prod),tuple(list_section),user_id))
				res = self.env.cr.dictfetchall()
				for opportunity in res :
					values_lost = opportunity.get('count')
					user = opportunity.get('user_id')
					user_name = self.env['res.users'].browse(user).name
					data.append({'label':user_name, 'value':values_lost,'id':self.id})
				return [{'values': data, 'area': True}]

    #######################APRÈS VENTE"""""Nombre d'opportunité gagné par département
    @api.multi
    def get_dashboard_change_opportunity_won_dep(self):
	data = []
	list_prod = []
	list_section = []
 	if self.type_dash == 'op_dep_won' :
		###utilisateur en cours"
		user_id = self.env['res.users'].browse(self.env.uid).id
		###si chef
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		##Liste des produits à suivre
		product_ids = self.env['product.template'].search([('a_suivre','=',True)])
		for product in product_ids :
			list_prod.append(product.id)

		
		if user_id == 1 : #pour l'administrateur
			section_ids = self.env['crm.case.section'].search([])
			for section_id in section_ids :
				section_name = self.env['crm.case.section'].browse(section_id.id).name
			if list_prod :
				self.env.cr.execute("SELECT COUNT(id) FROM crm_lead WHERE stage_id=%s AND product_id in %s",(6,tuple(list_prod)))
				res = self.env.cr.dictfetchall()
				for i in res:
					values_dep_won = i.get('count')
					data.append({'label':section_name, 'value':values_dep_won,'id':self.id})

				return [{'values': data, 'area': True,'id': self.id}]

		elif section_ids: #pour le chef du département
			for section in section_ids:
				section_name = self.env['crm.case.section'].browse(section.id).name
				list_section.append(section.id)
			if list_prod :
				self.env.cr.execute("SELECT COUNT(id) FROM crm_lead WHERE stage_id=%s AND product_id in %s AND section_id in %s ",(6,tuple(list_prod),tuple(list_section)))
				res = self.env.cr.dictfetchall()
				for i in res:
					values_dep_won = i.get('count')
					data.append({'label':section_name, 'value':values_dep_won,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

		else : #pour le commercial
			section_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
			for section in section_ids:
				section_name = self.env['crm.case.section'].browse(section.id).name
				list_section.append(section.id)
			if list_prod :
				self.env.cr.execute("SELECT COUNT(id) FROM crm_lead WHERE user_id =%s AND stage_id=%s AND product_id in %s AND section_id in %s",(user_id,6,tuple(list_prod),tuple(list_section)))
				res = self.env.cr.dictfetchall()
				for i in res:
					values_dep_won = i.get('count')
					data.append({'label':section_name, 'value':values_dep_won,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

    ########################APRÈS VENTE"""""Nombre d'opportunité perdu par département
    @api.multi
    def get_dashboard_change_opportunity_lost_dep(self):
	data = []
	list_prod = []
	list_section = []
 	if self.type_dash == 'op_dep_lost' :
		###utilisateur en cours"
		user_id = self.env['res.users'].browse(self.env.uid).id
		###si chef
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		##Liste des produits à suivre
		product_ids = self.env['product.template'].search([('a_suivre','=',True)])
		for product in product_ids :
			list_prod.append(product.id)
		if list_prod :
			if user_id == 1 : #pour l'administrateur
				section_ids = self.env['crm.case.section'].search([])
				for section_id in section_ids :
					section_name = self.env['crm.case.section'].browse(section_id.id).name
				
				self.env.cr.execute("SELECT COUNT(id) FROM crm_lead WHERE stage_id=%s AND product_id in %s",(7,tuple(list_prod)))
				res = self.env.cr.dictfetchall()
				for i in res:
					values_dep_lost = i.get('count')
					data.append({'label':section_name, 'value':values_dep_lost,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]
			elif section_ids: #pour le chef du département
				for section in section_ids:
					section_name = self.env['crm.case.section'].browse(section.id).name
					list_section.append(section.id)
				self.env.cr.execute("SELECT COUNT(id) FROM crm_lead WHERE stage_id=%s AND product_id in %s AND section_id in %s ",(7,tuple(list_prod),tuple(list_section)))
				res = self.env.cr.dictfetchall()
				for i in res:
					values_dep_lost = i.get('count')
					data.append({'label':section_name, 'value':values_dep_lost,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]
			else : #pour le commercial
				section_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
				for section in section_ids:
					section_name = self.env['crm.case.section'].browse(section.id).name
					list_section.append(section.id)
				self.env.cr.execute("SELECT COUNT(id) FROM crm_lead WHERE stage_id=%s AND product_id in %s AND section_id in %s ",(7,tuple(list_prod),tuple(list_section)))
				res = self.env.cr.dictfetchall()
				for i in res:
					values_dep_lost = i.get('count')
					data.append({'label':section_name, 'value':values_dep_lost,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]



    #################AVANT VENTE Vision Financière par état
    @api.multi
    def get_dashboard_vision_state(self):
	data = []
	list_prod = []
	list_section=[]
	value = 0
 	if self.type_dash == 'vision_state' :
		user_id = self.env['res.users'].browse(self.env.uid).id
		print '....user_id...',user_id
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])

		if user_id == 1 : #pour l'administrateur
			print "pour l'administrateur........................."

			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
			if list_prod :
				self.env.cr.execute("SELECT SUM(planned_revenue), stage_id FROM crm_lead WHERE product_id in %s AND stage_id NOT IN %s GROUP BY stage_id",(tuple(list_prod),(6,7)))
				res = self.env.cr.dictfetchall()
				for i in res:
					stage_id = i['stage_id']
					value = i.get('sum')
					state = self.env['crm.case.stage'].browse(stage_id).name
					data.append({'label':state , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

		elif section_ids :  #pour le chef du département
			print 'pour le chef du département......................'

			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)

			for section in section_ids:
				print "...dep..",section
				list_section.append(section.id)
			if list_prod :
				self.env.cr.execute("SELECT SUM(planned_revenue), stage_id FROM crm_lead WHERE product_id in %s AND section_id in %s AND stage_id NOT IN %s GROUP BY stage_id",(tuple(list_prod),tuple(list_section),(6,7)))
				res = self.env.cr.dictfetchall()
				for i in res:
					stage_id = i['stage_id']
					value = i.get('sum')
					state = self.env['crm.case.stage'].browse(stage_id).name
					data.append({'label':state , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

		else : #pour le commercial
			print 'pour le commercial .......................'

			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
			if list_prod :
				self.env.cr.execute("SELECT SUM(planned_revenue), stage_id FROM crm_lead WHERE product_id in %s AND user_id =%s AND stage_id NOT IN %s GROUP BY stage_id",(tuple(list_prod),user_id,(6,7)))
				res = self.env.cr.dictfetchall()
				for i in res:
					stage_id = i['stage_id']
					value = i.get('sum')
					state = self.env['crm.case.stage'].browse(stage_id).name
					data.append({'label':state , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]




    #################AVANT VENTE Vision Financière par département
    @api.multi
    def get_dashboard_vision_dep(self):
	data = []
	list_prod = []
	list_section = []
	value = 0
 	if self.type_dash == 'vision_dep' :
		user_id = self.env['res.users'].browse(self.env.uid).id
		print '....user_id...',user_id
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])

		if user_id == 1 : #pour l'administrateur
			print "pour l'administrateur........................."
			##Liste des produits à suivre
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
			if list_prod :
				list_section_ids = self.env['crm.case.section'].search([])
				for section_id in list_section_ids :
					section_name = self.env['crm.case.section'].browse(section_id.id).name

					self.env.cr.execute("SELECT SUM(planned_revenue) FROM crm_lead WHERE product_id in %s AND section_id = %s AND stage_id NOT IN %s ",(tuple(list_prod), section_id.id,(6,7)))
					res = self.env.cr.dictfetchall()
					for i in res:
						value = i.get('sum')
						data.append({'label':section_name , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

		elif section_ids :  #pour le chef du département
			print 'pour le chef du département......................'

			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
			if list_prod :
				for section in section_ids:
					print "...dep..",section
					section_name = self.env['crm.case.section'].browse(section.id).name
					list_section.append(section.id)

					self.env.cr.execute("SELECT SUM(planned_revenue) FROM crm_lead WHERE product_id in %s AND section_id = %s AND stage_id NOT IN %s ",(tuple(list_prod), section_id.id,(6,7)))
					res = self.env.cr.dictfetchall()
					for i in res:
						value = i.get('sum')
						data.append({'label':section_name , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

		else : #pour le commercial
			print 'pour le commercial .......................'
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
				
			if list_prod :
				section_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
				for section_id in section_ids :
					list_section.append(section_id.id)
					section_name = self.env['crm.case.section'].browse(section_id.id).name

					self.env.cr.execute("SELECT SUM(planned_revenue) FROM crm_lead WHERE product_id in %s AND section_id = %s AND stage_id NOT IN %s ",(tuple(list_prod), section_id.id,(6,7)))
					res = self.env.cr.dictfetchall()
					for i in res:
						value = i.get('sum')
						data.append({'label':section_name , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]


    #################AVANT VENTE Vision Financière par commercial
    @api.multi
    def get_dashboard_vision_ag(self):
	data = []
	list_prod = []
	list_section = []
	value = 0
 	if self.type_dash == 'vision_ag' :
		user_id = self.env['res.users'].browse(self.env.uid).id
		print '....user_id...',user_id
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])

		if user_id == 1 : #pour l'administrateur
			print "pour l'administrateur........................."
			##Liste des produits à suivre
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
			if list_prod :
				self.env.cr.execute("SELECT SUM(planned_revenue), user_id FROM crm_lead WHERE product_id in %s AND stage_id NOT IN %s GROUP BY user_id ",(tuple(list_prod),(6,7)))
				res = self.env.cr.dictfetchall()
				for i in res:
					user_id = i['user_id']
					user = self.env['res.users'].browse(user_id).name
					value = i.get('sum')
					data.append({'label':user , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

		elif section_ids :  #pour le chef du département
			print 'pour le chef du département......................'
			##Liste des produits à suivre
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)

			section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
			for section_id in section_ids :
				list_section.append(section_id.id)
				
			if list_prod :
				self.env.cr.execute("SELECT SUM(planned_revenue), user_id FROM crm_lead WHERE product_id in %s AND section_id in %s AND stage_id NOT IN %s GROUP BY user_id",(tuple(list_prod),tuple(list_section),(6,7)))
				res = self.env.cr.dictfetchall()
				for i in res:
					user_id = i['user_id']
					user = self.env['res.users'].browse(user_id).name
					value = i.get('sum')
					data.append({'label':user , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

		else : #pour le commercial
			print 'pour le commercial .......................'
			##Liste des produits à suivre
			product_ids = self.env['product.template'].search([('a_suivre','=',True)])
			for product in product_ids :
				list_prod.append(product.id)
			section_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
			for section_id in section_ids :
				list_section.append(section_id.id)
			if list_prod :
				self.env.cr.execute("SELECT SUM(planned_revenue), user_id FROM crm_lead WHERE product_id in %s AND user_id=%s AND stage_id NOT IN %s GROUP BY user_id",(tuple(list_prod),user_id,(6,7)))
				res = self.env.cr.dictfetchall()
				for i in res:
					user = self.env['res.users'].browse(user_id).name
					value = i.get('sum')
					data.append({'label':user , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

    #################AVANT VENTE Chiffre d'affaire gagné 
    @api.multi
    def get_dashboard_ca_ag(self):
	data = []
	list_prod = []
	list_section = []
	value = 0
 	if self.type_dash == 'chiffre' :
		user_id = self.env['res.users'].browse(self.env.uid).id
		##Liste des produits à suivre
		product_ids = self.env['product.template'].search([('a_suivre','=',True)])
		for product in product_ids :
			list_prod.append(product.id)
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		
		if list_prod :
			if user_id == 1 : #pour l'administrateur
				section_ids = self.env['crm.case.section'].search([])
				for section in section_ids:
					self.env.cr.execute("SELECT SUM(planned_revenue), section_id FROM crm_lead WHERE product_id in %s AND stage_id =%s AND section_id =%s GROUP BY section_id",(tuple(list_prod),6,section.id))
					res = self.env.cr.dictfetchall()
					for i in res:
						value = i.get('sum')
						section_id = i.get('section_id')
						section_name = self.env['crm.case.section'].browse(section_id).name
						data.append({'label':section_name , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

			elif section_ids :  #pour le chef du département
				
				for section in section_ids:
					list_section.append(section.id)
					section_name = self.env['crm.case.section'].browse(section.id).name
					self.env.cr.execute("SELECT SUM(planned_revenue) FROM crm_lead WHERE product_id in %s AND stage_id =%s AND section_id = %s ",(tuple(list_prod),6,section.id))
					res = self.env.cr.dictfetchall()
					for i in res:
						value = i.get('sum')
						data.append({'label':section_name , 'value':value,'id':self.id})
					
				return [{'values': data, 'area': True,'id': self.id}]

			else : #pour le commercial
				section_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
				for section in section_ids:
					self.env.cr.execute("SELECT SUM(planned_revenue) FROM crm_lead WHERE product_id in %s AND stage_id =%s AND section_id = %s ",(tuple(list_prod),6,section.id))
					res = self.env.cr.dictfetchall()
					for i in res:
						value = i.get('sum')
						section_name = self.env['crm.case.section'].browse(section.id).name
						print 'pour le commercial .......................',section_name
						data.append({'label':section_name , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]
		
    #################AVANT VENTE Chiffre d'affaire prévisible par département 
    @api.multi
    def get_dashboard_ca_dep(self):
	data = []
	list_prod = []
	list_section = []

 	if self.type_dash == 'ca_dep' :
		user_id = self.env['res.users'].browse(self.env.uid).id
		##Liste des produits à suivre
		product_ids = self.env['product.template'].search([('a_suivre','=',True)])
		for product in product_ids :
			list_prod.append(product.id)

		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		if list_prod :
			if user_id == 1 : #pour l'administrateur
				section_ids = self.env['crm.case.section'].search([])
				for section_id in section_ids :
					list_section.append(section_id.id)
					section_name = self.env['crm.case.section'].browse(section_id.id).name
					invoiced_target = self.env['crm.case.section'].browse(section_id.id).invoiced_target
					data.append({'label':section_name , 'value':invoiced_target,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

			elif section_ids :  #pour le chef du département
				for section_id in section_ids :
					list_section.append(section_id.id)
					section_name = self.env['crm.case.section'].browse(section_id.id).name
					invoiced_target = self.env['crm.case.section'].browse(section_id.id).invoiced_target
					data.append({'label':section_name , 'value':invoiced_target,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

			else : #pour le commercial
				section_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
				for section_id in section_ids :
					list_section.append(section_id.id)
					invoiced_target = self.env['crm.case.section'].browse(section_id.id).invoiced_target
					section_name = self.env['crm.case.section'].browse(section_id.id).name

					data.append({'label':section_name , 'value':invoiced_target,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]
##############""""
    @api.multi
    def get_dashboard_top_ten(self):
	data = []
	list_prod = []
	value = 0
	j=0


	###get last 12 months
	x = 12
	today = date.today() 
	now = time.localtime()
	last_date = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, now.tm_mday , 0, 0, 0, 0, 0, 0)))[:3] for n in range(x)]
	last = last_date[9]
	last_months = date(*last[:3])

 	if self.type_dash == 'operateur' :
		 ##Liste des produits à suivre
		product_ids = self.env['product.template'].search([('a_suivre','=',True)])
		for product in product_ids :
			list_prod.append(product.id)

		user_id = self.env['res.users'].browse(self.env.uid).id
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		if list_prod :
			if user_id == 1 : #pour l'administrateur
				self.env.cr.execute("SELECT COUNT(id), partner_id FROM crm_lead WHERE product_id in %s AND stage_id=%s AND date_debut >= %s AND date_fin <= %s GROUP BY partner_id ORDER BY COUNT(id) DESC",(tuple(list_prod),6,last_months,today))
				res = self.env.cr.dictfetchall()


				for i in res:
					j = j+1
					if j<=10 :
						partner_id = i['partner_id']
						partner = self.env['res.partner'].browse(partner_id).name
						value = i.get('count')
						data.append({'label':partner , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

			elif section_ids :  #pour le chef du département
				self.env.cr.execute("SELECT COUNT(id), partner_id FROM crm_lead WHERE product_id in %s AND stage_id=%s AND date_debut >= %s AND date_fin <= %s GROUP BY partner_id ORDER BY COUNT(id) DESC",(tuple(list_prod),6,last_months,today))
				res = self.env.cr.dictfetchall()

				for i in res:
					j = j+1
					if j<=10 :
						partner_id = i['partner_id']
						partner = self.env['res.partner'].browse(partner_id).name
						value = i.get('count')
						data.append({'label':partner , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]
			else : #pour le commercial
				self.env.cr.execute("SELECT COUNT(id), partner_id FROM crm_lead WHERE product_id in %s AND stage_id=%s AND date_debut >= %s AND date_fin <= %s GROUP BY partner_id ORDER BY COUNT(id) DESC",(tuple(list_prod),6,last_months,today))
				res = self.env.cr.dictfetchall()
				n = len(res)
				for i in res:
					j = j+1
					if j<=10 :
						partner_id = i['partner_id']
						partner = self.env['res.partner'].browse(partner_id).name
						value = i.get('count')
						data.append({'label':partner , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]
##############"TOP 10 chiffre d'affaire par opéarateur 
    @api.multi
    def get_dashboard_top_ten_revenue(self):
	data = []
	list_prod = []
	value = 0
	j=0


	###get last 12 months
	x = 12
	today = date.today() 
	now = time.localtime()
	last_date = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, now.tm_mday , 0, 0, 0, 0, 0, 0)))[:3] for n in range(x)]
	last = last_date[9]
	last_months = date(*last[:3])

 	if self.type_dash == 'operateur_revenue' :
		 ##Liste des produits à suivre
		product_ids = self.env['product.template'].search([('a_suivre','=',True)])
		for product in product_ids :
			list_prod.append(product.id)

		user_id = self.env['res.users'].browse(self.env.uid).id
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		if list_prod :
			if user_id == 1 : #pour l'administrateur
				self.env.cr.execute("SELECT SUM(planned_revenue), partner_id FROM crm_lead WHERE product_id in %s AND stage_id=%s AND date_debut >= %s AND date_fin <= %s GROUP BY partner_id ORDER BY COUNT(id) DESC",(tuple(list_prod),6,last_months,today))
				res = self.env.cr.dictfetchall()


				for i in res:
					j = j+1
					if j<=10 :
						partner_id = i['partner_id']
						partner = self.env['res.partner'].browse(partner_id).name
						value = i.get('sum')
						data.append({'label':partner , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

			elif section_ids :  #pour le chef du département
				self.env.cr.execute("SELECT SUM(planned_revenue), partner_id FROM crm_lead WHERE product_id in %s AND stage_id=%s AND date_debut >= %s AND date_fin <= %s GROUP BY partner_id ORDER BY COUNT(id) DESC",(tuple(list_prod),6,last_months,today))
				res = self.env.cr.dictfetchall()

				for i in res:
					j = j+1
					if j<=10 :
						partner_id = i['partner_id']
						partner = self.env['res.partner'].browse(partner_id).name
						value = i.get('sum')
						data.append({'label':partner , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]
			else : #pour le commercial
				self.env.cr.execute("SELECT SUM(planned_revenue), partner_id FROM crm_lead WHERE product_id in %s AND stage_id=%s AND date_debut >= %s AND date_fin <= %s GROUP BY partner_id ORDER BY COUNT(id) DESC",(tuple(list_prod),6,last_months,today))
				res = self.env.cr.dictfetchall()
				n = len(res)
				for i in res:
					j = j+1
					if j<=10 :
						partner_id = i['partner_id']
						partner = self.env['res.partner'].browse(partner_id).name
						value = i.get('sum')
						data.append({'label':partner , 'value':value,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]
 #######################"""""Nombre d'opportunité gagné par commercial durant ces derniers 30 jours
    @api.multi
    def get_dashboard_change_opportunity_won_period(self):
	data = []
	list_prod = []
	list_section = []
	today = date.today()
	if today.month == 1:
		date_from = date(today.year - 1)
	else:
		date_from = date(today.year,today.month - 1,today.day)
	##Liste des produits à suivre
	product_ids = self.env['product.template'].search([('a_suivre','=',True)])
	for product in product_ids :
		list_prod.append(product.id)

 	if self.type_dash == 'period_won' :
		user_id = self.env['res.users'].browse(self.env.uid).id
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		if list_prod:
			if user_id == 1 : #pour l'administrateur
				self.env.cr.execute("SELECT COUNT(id), user_id FROM crm_lead WHERE stage_id=%s AND product_id in %s AND date_fin <= %s AND date_debut >= %s GROUP BY user_id",(6,tuple(list_prod),date.today(),date_from))
				res = self.env.cr.dictfetchall()
				for i in res:
					user_id = i['user_id']
					values_won = i.get('count')
					user = self.env['res.users'].browse(user_id).name
					data.append({'label':user, 'value':values_won,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

			elif section_ids :  #pour le chef du département'


				for section in section_ids:
					list_section.append(section.id)
				
				self.env.cr.execute("SELECT COUNT(id), user_id FROM crm_lead WHERE stage_id=%s AND product_id in %s AND date_fin <= %s AND date_debut >= %s AND section_id in %s GROUP BY user_id",(6,tuple(list_prod),date.today(),date_from,tuple(list_section),))
				opportunity_won_ids = self.env.cr.dictfetchall()
				for opportunity in opportunity_won_ids :
					values_won = opportunity.get('count')
					user_id = opportunity.get('user_id')
					user = self.env['res.users'].browse(user_id).name
					data.append({'label':user, 'value':values_won,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

			else : #pour le commercial
				section_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
				for section in section_ids:
					list_section.append(section.id)

				self.env.cr.execute("SELECT COUNT(id) FROM crm_lead WHERE user_id =%s AND stage_id=%s AND product_id in %s AND date_fin <= %s AND date_debut >= %s AND section_id in %s",(user_id,6,tuple(list_prod),date.today(),date_from,tuple(list_section),))
				opportunity_won_ids = self.env.cr.dictfetchall()
				for opportunity in opportunity_won_ids :
					values_won = opportunity.get('count')
					user = self.env['res.users'].browse(user_id).name
					data.append({'label':user, 'value':values_won,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]



#######""

	#################################### Nombre d'opportunité perdu par commercial durant ces derniers 30 jours
    @api.multi
    def get_dashboard_change_opportunity_lost_period(self):
	data = []
	list_prod = []
	list_section = []
	today = date.today()
	if today.month == 1:
		date_from = date(today.year - 1)
	else:
		date_from = date(today.year,today.month - 1,today.day)
	##Liste des produits à suivre
	product_ids = self.env['product.template'].search([('a_suivre','=',True)])
	for product in product_ids :
		list_prod.append(product.id)

 	if self.type_dash == 'period_lost' :
		user_id = self.env['res.users'].browse(self.env.uid).id
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		if list_prod:
			if user_id == 1 : #pour l'administrateur
				self.env.cr.execute("SELECT COUNT(id), user_id FROM crm_lead WHERE stage_id=%s AND product_id in %s AND date_fin <= %s AND date_debut >= %s GROUP BY user_id",(7,tuple(list_prod),date.today(),date_from))
				res = self.env.cr.dictfetchall()
				for i in res:
					user_id = i['user_id']
					values_lost = i.get('count')
					user = self.env['res.users'].browse(user_id).name
					data.append({'label':user, 'value':values_lost,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

			elif section_ids :  #pour le chef du département
				for section in section_ids:
					list_section.append(section.id)
		
				self.env.cr.execute("SELECT COUNT(id), user_id FROM crm_lead WHERE stage_id=%s AND product_id in %s AND date_fin <= %s AND date_debut >= %s AND section_id in %s GROUP BY user_id",(7,tuple(list_prod),date.today(),date_from,tuple(list_section),))
				opportunity_lost_ids = self.env.cr.dictfetchall()
				for opportunity in opportunity_lost_ids :
					values_lost = opportunity.get('count')
					user_id = opportunity.get('user_id')
					user = self.env['res.users'].browse(user_id).name
					data.append({'label':user, 'value':values_lost,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

			else : #pour le commercial
				section_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
				for section in section_ids:
					list_section.append(section.id)

				self.env.cr.execute("SELECT COUNT(id) FROM crm_lead WHERE stage_id=%s AND product_id in %s AND date_fin <= %s AND date_debut >= %s AND section_id in %s",(7,tuple(list_prod),date.today(),date_from,tuple(list_section),))
				opportunity_lost_ids = self.env.cr.dictfetchall()
				for opportunity in opportunity_lost_ids :
					values_lost = opportunity.get('count')
					user = self.env['res.users'].browse(user_id).name
					data.append({'label':user, 'value':values_lost,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]


####################################" Nombre d'opportunité gangné par département durant ces derniers 30 jours
    @api.multi
    def get_dashboard_change_opportunity_won_dep_period(self):
	data = []
	list_prod = []

	today = date.today()
	if today.month == 1:
		date_from = date(today.year - 1)
	else:
		date_from = date(today.year,today.month - 1,today.day)
	
 	if self.type_dash == 'op_won' :
		user_id = self.env['res.users'].browse(self.env.uid).id
		##Liste des produits à suivre
		product_ids = self.env['product.template'].search([('a_suivre','=',True)])
		for product in product_ids :
			list_prod.append(product.id)
		
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		if list_prod:
			if user_id == 1 : #pour l'administrateur
				section_ids = self.env['crm.case.section'].search([])
				for section_id in section_ids :
					section_name = self.env['crm.case.section'].browse(section_id.id).name
					self.env.cr.execute("SELECT COUNT(id) FROM crm_lead WHERE section_id =%s AND stage_id=%s AND product_id in %s  AND date_fin <= %s AND date_debut >= %s",(section_id.id,6,tuple(list_prod),date.today(),date_from))
					res = self.env.cr.dictfetchall()
					for i in res:
						values_dep_won = i.get('count')
					data.append({'label':section_name, 'value':values_dep_won,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]
			elif section_ids:
				for section_id in section_ids :
					section_name = self.env['crm.case.section'].browse(section_id.id).name
					self.env.cr.execute("SELECT COUNT(id) FROM crm_lead WHERE section_id =%s AND stage_id=%s AND product_id in %s  AND date_fin <= %s AND date_debut >= %s",(section_id.id,6,tuple(list_prod),date.today(),date_from))
					res = self.env.cr.dictfetchall()
					for i in res:
						values_dep_won = i.get('count')
					data.append({'label':section_name, 'value':values_dep_won,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]
			else :
				section_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
				for section_id in section_ids :
					section_name = self.env['crm.case.section'].browse(section_id.id).name
					self.env.cr.execute("SELECT COUNT(id) FROM crm_lead WHERE section_id =%s AND stage_id=%s AND product_id in %s  AND date_fin <= %s AND date_debut >= %s",(section_id.id,6,tuple(list_prod),date.today(),date_from))
					res = self.env.cr.dictfetchall()
					for i in res:
						values_dep_won = i.get('count')
					data.append({'label':section_name, 'value':values_dep_won,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

    ######################## Nombre d'opportunité perdu par département durant ces derniers 30 jours
    @api.multi
    def get_dashboard_change_opportunity_lost_dep_period(self):
	data = []
	list_prod = []

	today = date.today()
	if today.month == 1:
		date_from = date(today.year - 1)
	else:
		date_from = date(today.year,today.month - 1,today.day)
	

 	if self.type_dash == 'op_lost' :
		user_id = self.env['res.users'].browse(self.env.uid).id
		##Liste des produits à suivre
		product_ids = self.env['product.template'].search([('a_suivre','=',True)])
		for product in product_ids :
			list_prod.append(product.id)
		
		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		if list_prod:
			if user_id == 1 : #pour l'administrateur
				section_ids = self.env['crm.case.section'].search([])
				for section_id in section_ids :
					self.env.cr.execute("SELECT COUNT(id) FROM crm_lead WHERE section_id =%s AND stage_id=%s AND product_id in %s  AND date_fin <= %s AND date_debut >= %s",(section_id.id,7,tuple(list_prod),date.today(),date_from))
					res = self.env.cr.dictfetchall()
					for i in res:
						values_dep_won = i.get('count')
						section_name = self.env['crm.case.section'].browse(section_id.id).name
					data.append({'label':section_name, 'value':values_dep_won,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]
			elif section_ids:
				for section_id in section_ids :
					self.env.cr.execute("SELECT COUNT(id) FROM crm_lead WHERE section_id =%s AND stage_id=%s AND product_id in %s  AND date_fin <= %s AND date_debut >= %s",(section_id.id,7,tuple(list_prod),date.today(),date_from))
					res = self.env.cr.dictfetchall()
					for i in res:
						section_name = self.env['crm.case.section'].browse(section_id.id).name
						values_dep_won = i.get('count')
					data.append({'label':section_name, 'value':values_dep_won,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]
			else :
				section_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
				for section_id in section_ids :
					self.env.cr.execute("SELECT COUNT(id) FROM crm_lead WHERE section_id =%s AND stage_id=%s AND product_id in %s  AND date_fin <= %s AND date_debut >= %s",(section_id.id,7,tuple(list_prod),date.today(),date_from))
					res = self.env.cr.dictfetchall()
					for i in res:
						section_name = self.env['crm.case.section'].browse(section_id.id).name
						values_dep_won = i.get('count')
					data.append({'label':section_name, 'value':values_dep_won,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]
