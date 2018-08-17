#-*- coding:utf-8 -*-
import json
from datetime import date, datetime, timedelta
import calendar
from babel.dates import format_datetime, format_date
from openerp import models, api, _, fields
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class crm_dashboard_activity(models.Model):
    _name = "crm.dashboard.activity"

    @api.one
    def _kanban_dashboard(self):
        self.kanban_dashboard = json.dumps(self.get_journal_dashboard_datas())


    @api.one
    def _dashboard_activity_email(self):
		self.dashboard_activity_email = json.dumps(self.get_dashboard_activity_email())
    @api.one
    def _dashboard_activity_appel(self):
		self.dashboard_opportunity_appel = json.dumps(self.get_dashboard_activity_appel())
    @api.one
    def _dashboard_activity_reunion(self):
		self.dashboard_activity_reunion = json.dumps(self.get_dashboard_activity_reunion())

    name = fields.Char(string='Name') 
    type_dash = fields.Selection([('email', "email"),('appel', "appel"),('reunion', "reunion")])
    kanban_dashboard = fields.Text(compute='_kanban_dashboard')

    dashboard_activity_email = fields.Text(compute='_dashboard_activity_email')
    dashboard_activity_appel = fields.Text(compute='_dashboard_activity_appel')
    dashboard_activity_reunion = fields.Text(compute='_dashboard_activity_reunion')


    show_on_dashboard = fields.Boolean(string='Show journal on dashboard', help="Whether this journal should be displayed on the dashboard or not", default=True)


    @api.multi
    def get_journal_dashboard_datas(self):
	print "u call get_journal_dashboard_datas"


    ##Nombre d'email envoyé par activité
    @api.multi
    def get_dashboard_activity_email(self):
	data = []
	list_prod = []
	list_opportunity = []
	list_section = []
	list_opportunity_chef = []
	list_opportunity_comm = []
	list_section_comm = []

 	if self.type_dash == 'email' :
		user_id = self.env['res.users'].browse(self.env.uid).id
		##Liste des produits à suivre
		product_ids = self.env['product.template'].search([('a_suivre','=',True)])
		if product_ids :
			for product in product_ids :
				list_prod.append(product.id)
		
		opportunity_ids = self.env['crm.lead'].search([('product_id','in',tuple(list_prod))])
		if opportunity_ids:
			for opportunity in opportunity_ids :
				list_opportunity.append(opportunity.id)


		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		if section_ids:
			for section in section_ids:
				list_section.append(section.id)
		opportunity_chef_ids = self.env['crm.lead'].search([('product_id','in',tuple(list_prod)),('section_id','in',tuple(list_section))])
		if opportunity_chef_ids:
			for opportunity in opportunity_chef_ids :
				list_opportunity_chef.append(opportunity.id)

		section_commercial_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
		if section_commercial_ids:
			for section in section_commercial_ids:
				list_section_comm.append(section.id)
		opportunity_comm_ids = self.env['crm.lead'].search([('product_id','in',tuple(list_prod)),('section_id','in',tuple(list_section_comm))])
		if opportunity_comm_ids:
			for opportunity in opportunity_comm_ids :
				list_opportunity_comm.append(opportunity.id)

		if list_opportunity and user_id == 1:
			 #pour l'administrateur
			self.env.cr.execute("SELECT COUNT(id), mail_message_id FROM mail_mail WHERE state =%s AND opportunity_ids in %s GROUP BY mail_message_id",("sent",tuple(list_opportunity)))

			res = self.env.cr.dictfetchall()
			for i in res:
				mail_message_id = i['mail_message_id']
				nb_mail = i.get('count')
				print "nb_mail",nb_mail
				self.env.cr.execute("SELECT subject FROM mail_message WHERE id =%s",(mail_message_id,))
				result = self.env.cr.dictfetchall()
				for s in result:
					activity = s['subject']

					data.append({'label':activity , 'value':nb_mail,'id':self.id})
			print '....',data
			return [{'values': data, 'area': True,'id': self.id}]

		if list_opportunity_chef: #pour le chef du département
			self.env.cr.execute("SELECT COUNT(id), mail_message_id FROM mail_mail WHERE state =%s AND opportunity_ids in %s GROUP BY mail_message_id",("sent",tuple(list_opportunity_chef)))

			res = self.env.cr.dictfetchall()
			for i in res:
				mail_message_id = i['mail_message_id']
				nb_mail = i.get('count')
				print "nb_mail",nb_mail
				self.env.cr.execute("SELECT subject FROM mail_message WHERE id =%s",(mail_message_id,))
				result = self.env.cr.dictfetchall()
				for s in result:
					activity = s['subject']

					data.append({'label':activity , 'value':nb_mail,'id':self.id})
			print '....',data
			return [{'values': data, 'area': True,'id': self.id}]

		if list_opportunity_comm : #pour le commercial
			self.env.cr.execute("SELECT COUNT(id), mail_message_id FROM mail_mail WHERE state =%s AND opportunity_ids in %s GROUP BY mail_message_id",("sent",tuple(list_opportunity_comm)))
			res = self.env.cr.dictfetchall()
			for i in res:
				mail_message_id = i['mail_message_id']
				nb_mail = i.get('count')
				print "nb_mail",nb_mail
				self.env.cr.execute("SELECT subject FROM mail_message WHERE id =%s",(mail_message_id,))
				result = self.env.cr.dictfetchall()
				for s in result:
					activity = s['subject']

					data.append({'label':activity , 'value':nb_mail,'id':self.id})
			print '....',data

    ##Nombre d'appel envoyé par activité
    @api.multi
    def get_dashboard_activity_appel(self):
	data = []
	list_prod = []
	list_opportunity = []
	list_section = []
	list_opportunity_chef = []
	list_opportunity_comm = []
	list_section_comm = []
 	if self.type_dash == 'appel' :
		user_id = self.env['res.users'].browse(self.env.uid).id
		##Liste des produits à suivre
		product_ids = self.env['product.template'].search([('a_suivre','=',True)])
		if product_ids :
			for product in product_ids :
				list_prod.append(product.id)
		
		opportunity_ids = self.env['crm.lead'].search([('product_id','in',tuple(list_prod))])
		if opportunity_ids:
			for opportunity in opportunity_ids :
				list_opportunity.append(opportunity.id)


		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		if section_ids:
			for section in section_ids:
				list_section.append(section.id)
		opportunity_chef_ids = self.env['crm.lead'].search([('product_id','in',tuple(list_prod)),('section_id','in',tuple(list_section))])
		if opportunity_chef_ids:
			for opportunity in opportunity_chef_ids :
				list_opportunity_chef.append(opportunity.id)

		section_commercial_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
		if section_commercial_ids:
			for section in section_commercial_ids:
				list_section_comm.append(section.id)

		opportunity_comm_ids = self.env['crm.lead'].search([('product_id','in',tuple(list_prod)),('section_id','in',tuple(list_section_comm))])
		if opportunity_comm_ids:
			for opportunity in opportunity_comm_ids :
				list_opportunity_comm.append(opportunity.id)

		opportunity_ids = self.env['crm.lead'].search([('product_id','in',tuple(list_prod))])
		if opportunity_ids:
			for opportunity in opportunity_ids :
				list_opportunity.append(opportunity.id)

		if list_opportunity and user_id == 1:
			#pour l'administrateur:
			self.env.cr.execute("SELECT COUNT(id), mail_message_id FROM mail_mail WHERE state =%s AND opportunity_ids in %s GROUP BY mail_message_id",("sent",tuple(list_opportunity)))
			res = self.env.cr.dictfetchall()
			for i in res:
				mail_message_id = i['mail_message_id']
				nb_mail = i.get('count')
				self.env.cr.execute("SELECT subject FROM mail_message WHERE id =%s",(mail_message_id,))
				result = self.env.cr.dictfetchall()
				for s in result:
					activity = s['subject']

					data.append({'label':activity , 'value':nb_mail,'id':self.id})
			return [{'values': data, 'area': True,'id': self.id}]
		if list_opportunity_chef :
			self.env.cr.execute("SELECT COUNT(id), mail_message_id FROM mail_mail WHERE state =%s AND opportunity_ids in %s GROUP BY mail_message_id",("sent",tuple(list_opportunity_chef)))
			res = self.env.cr.dictfetchall()
			for i in res:
				mail_message_id = i['mail_message_id']
				nb_mail = i.get('count')
				self.env.cr.execute("SELECT subject FROM mail_message WHERE id =%s",(mail_message_id,))
				result = self.env.cr.dictfetchall()
				for s in result:
					activity = s['subject']

					data.append({'label':activity , 'value':nb_mail,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]
		if list_opportunity_comm :
			self.env.cr.execute("SELECT COUNT(id), mail_message_id FROM mail_mail WHERE state =%s AND opportunity_ids in %s GROUP BY mail_message_id",("sent",tuple(list_opportunity_comm)))
			res = self.env.cr.dictfetchall()
			for i in res:
				mail_message_id = i['mail_message_id']
				nb_mail = i.get('count')
				self.env.cr.execute("SELECT subject FROM mail_message WHERE id =%s",(mail_message_id,))
				result = self.env.cr.dictfetchall()
				for s in result:
					activity = s['subject']

					data.append({'label':activity , 'value':nb_mail,'id':self.id})
				return [{'values': data, 'area': True,'id': self.id}]

    ##Nombre de reunion par activité
    @api.multi
    def get_dashboard_activity_reunion(self):
	data = []
	list_prod = []
	list_opportunity = []
	list_section = []
	list_opportunity_chef = []
	list_opportunity_comm = []
	list_section_comm = []
 	if self.type_dash == 'reunion' :
		user_id = self.env['res.users'].browse(self.env.uid).id
		##Liste des produits à suivre
		product_ids = self.env['product.template'].search([('a_suivre','=',True)])
		if product_ids :
			for product in product_ids :
				list_prod.append(product.id)
		
		opportunity_ids = self.env['crm.lead'].search([('product_id','in',tuple(list_prod))])
		if opportunity_ids:
			for opportunity in opportunity_ids :
				list_opportunity.append(opportunity.id)


		section_ids = self.env['crm.case.section'].search([('user_id','=',user_id)])
		if section_ids:
			for section in section_ids:
				list_section.append(section.id)
		opportunity_chef_ids = self.env['crm.lead'].search([('product_id','in',tuple(list_prod)),('section_id','in',tuple(list_section))])
		if opportunity_chef_ids:
			for opportunity in opportunity_chef_ids :
				list_opportunity_chef.append(opportunity.id)

		section_commercial_ids = self.env['crm.case.section'].search([('member_ids','=',user_id)])
		if section_commercial_ids:
			for section in section_commercial_ids:
				list_section_comm.append(section.id)

		opportunity_comm_ids = self.env['crm.lead'].search([('product_id','in',tuple(list_prod)),('section_id','in',tuple(list_section_comm))])
		if opportunity_comm_ids:
			for opportunity in opportunity_comm_ids :
				list_opportunity_comm.append(opportunity.id)

		opportunity_ids = self.env['crm.lead'].search([('product_id','in',tuple(list_prod))])
		if opportunity_ids:
			for opportunity in opportunity_ids :
				list_opportunity.append(opportunity.id)
		##Liste des produits à suivre
		product_ids = self.env['product.template'].search([('a_suivre','=',True)])
		if product_ids:
			for product in product_ids :
				list_prod.append(product.id)

		opportunity_ids = self.env['crm.lead'].search([('product_id','in',tuple(list_prod))])
		if opportunity_ids:
			for opportunity in opportunity_ids :
				list_opportunity.append(opportunity.id)

		if list_opportunity and user_id == 1:
			#pour l'administrateur:
			self.env.cr.execute("SELECT COUNT(id), name FROM calendar_event WHERE opportunity_ids in %s GROUP BY name",(tuple(list_opportunity),))
			res = self.env.cr.dictfetchall()
			for i in res:
				nb_reunion = i.get('count')
				activity = i['name']
				data.append({'label':activity , 'value':nb_reunion,'id':self.id})
			return [{'values': data, 'area': True,'id': self.id}]
		if list_opportunity_chef :
			self.env.cr.execute("SELECT COUNT(id), name FROM calendar_event WHERE opportunity_ids in %s GROUP BY name",(tuple(list_opportunity_chef),))
			res = self.env.cr.dictfetchall()
			for i in res:
				nb_reunion = i.get('count')
				activity = i['name']
				data.append({'label':activity , 'value':nb_reunion,'id':self.id})
			return [{'values': data, 'area': True,'id': self.id}]

		if list_opportunity_comm :
			self.env.cr.execute("SELECT COUNT(id), name FROM calendar_event WHERE opportunity_ids in %s GROUP BY name",(tuple(list_opportunity_comm),))
			res = self.env.cr.dictfetchall()
			for i in res:
				nb_reunion = i.get('count')
				activity = i['name']
				data.append({'label':activity , 'value':nb_reunion,'id':self.id})
			return [{'values': data, 'area': True,'id': self.id}]



