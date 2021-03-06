# -*- coding: utf-8 -*-
from datetime import date, datetime
import time
from dateutil import relativedelta
from openerp import tools
from openerp.osv import fields, osv
from datetime import datetime
from openerp.tools.translate import _
from openerp.exceptions import Warning
import openerp

class crm_next_activity(osv.Model):
    _inherit = "crm.lead"
    _name= "crm.lead"

    _columns = {

        'type_act': fields.selection([
            ('Mail', "Email"),
            ('Appel', "Appel"),
	    ('Reunion',"Réunion"),
        ], 'Type'),

        'date_action': fields.datetime(string='Date début', select=True),
        'title_action': fields.char(),

    }



    def closed_action(self,cr,uid,ids,context=None):

	type_activity=self.browse(cr,uid,ids,context=context).type_act
        for operation in self.browse(cr, uid, ids, context=context):
            date_deadline = operation.date_deadline
            date_action = operation.date_action
            title_action = operation.title_action

	    #test sur les champs date
	    if  (date_deadline == False and  date_action == False):
		raise osv.except_osv(_('Ops Date requis!'), _('Veuillez saisir les dates.'))
	    else :
		#vider les champs date
		self.write(cr, uid, ids, {'date_deadline': False,'date_action': False,'title_action': False,'type_act': False})
        return True




    def show_activity(self,cr,uid,ids,context=None):
	type_activity=self.browse(cr,uid,ids,context=context).type_act

        for operation in self.browse(cr, uid, ids, context=context):
        	title_action = operation.title_action 
		partner_id = operation.partner_id.id
		#l'opportunité liée par l'opérateur économique
		opportunity_ids = self.search(cr, uid,[('partner_id', '=' ,partner_id),('title_action','=',title_action),('stage_id','!=',6),('stage_id','!=',7)], context=context)
		print 'opportunity_ids....',opportunity_ids
		#for opportunity_id in opportunity_ids :
			#print 'opportunity_id....',opportunity_id
		opportunity_id = self.browse(cr,uid,opportunity_ids,context=context).id
		name = operation.name #produit en question
        date_action = operation.date_action
	#'target': 'new' lose the create button ,
	if type_activity =="Appel" :


		return {
			'name': ('Appel'),
			'view_type': 'form',
			'view_mode': 'tree',
			'res_model': 'crm.phonecall',
			'view_id ref= crm_case_inbound_phone_tree_view_inherit':True,
        		'context': {'default_name': title_action,'default_partner_id':partner_id, 'default_opportunity_id':opportunity_id},
			'type': 'ir.actions.act_window',
			'target': 'current',
			'options': {'mode': 'edit'},
		}

	if type_activity =="Mail" :
		return {
			'name': ('Email'),
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'mail.mail',
			'view_id ref= view_mail_form_inherit':True,
            'context': {'default_subject': title_action,'default_recipient_ids':[partner_id],'default_opportunity_ids':opportunity_id},
			'type': 'ir.actions.act_window',
			'target': 'current',

		}


	if type_activity =="Reunion" :
		return {
			'name': ('Réunion'),
			'view_type': 'form',
			'view_mode': 'form,tree',
			'view_id ref= view_calendar_event_form_inherit':True,
        	'context': {'default_name': title_action,'default_partner_ids':[partner_id],'default_opportunity_ids':opportunity_id},
			'res_model': 'calendar.event',
			'type': 'ir.actions.act_window',
			'target': 'current',
		}



	return True






