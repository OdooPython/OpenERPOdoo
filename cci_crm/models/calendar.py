# -*- coding: utf-8 -*-
from datetime import date, datetime
from dateutil import relativedelta
from openerp import tools
from openerp.osv import fields, osv
from datetime import datetime
from openerp.tools.translate import _
from openerp.exceptions import Warning
import openerp

class calendar_event(osv.Model):
    _inherit = "calendar.event"
    _name = 'calendar.event'

    def get_coach_id(self, cr, uid, ids,context=None):
	coach_id=self.pool.get('hr.employee').browse(cr,uid,ids,context=context).coach_id
	return coach_id

    _columns = {
	'opportunity_ids': fields.many2one('crm.lead','Opportunité'),
	'partner_contact_id':fields.many2many('res.partner', string="Contacts"),
	'coach_id':fields.integer(),
    }
    _default = {'coach_id':get_coach_id,}

    def create(self, cr, uid, vals, context=None):
	print "...........vals",vals
	name=vals['name']



	if 'opportunity_ids' in vals: 
		start_datetime=vals['start_datetime']
		stop_datetime=vals['stop_datetime']
		opportunity_ids=vals['opportunity_ids']
		partner_id=vals['partner_contact_id'][0][2][0]
		val = {
			'name':name,
			'partner_id':partner_id,
			'date_deadline': stop_datetime,
			'date_action':start_datetime,
			'type':'Reunion',
			'opportunity_ids':opportunity_ids,
		    }
		inv_id = self.pool.get('crm.lead.activity').create(cr, uid, val)
		super(calendar_event, self).create(cr, uid, vals, context=context)
		#rendre les champs vides 22-09-2017
		self.pool.get('crm.lead').write(cr, uid, opportunity_ids, {'date_deadline': False,'date_action': False,'title_action': False,'type_act': False})
	else : 
		print "else....vals.........",vals
		super(calendar_event, self).create(cr, uid, vals, context=context)
		






    def create_attendees(self, cr, uid, ids, context=None):
	return False

    def closed_action_calendar(self, cr, uid, ids,context=None):
	calendar_id=self.browse(cr, uid, ids,context=context).id
	opportunity_ids=self.browse(cr, uid, ids,context=context).opportunity_ids.id

	return self.pool.get('crm.lead').write(cr, uid, opportunity_ids, {'date_deadline': False,'date_action': False,'title_action': False,'type_act': False})


    _default = {
	'partner_ids': lambda self, cr, uid, context: context.get('partner_ids', False),
    }
