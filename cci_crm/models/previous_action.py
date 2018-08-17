# -*- coding: utf-8 -*-

from datetime import date, datetime
from dateutil import relativedelta
from openerp import tools
from openerp.osv import fields, osv


class crm_previous_activity(osv.Model):
    _name = "crm.lead.activity"



    # def _get_coach_id(self,cr, uid, ids, field_name, arg, context=None):
    #     print 'u will call get coach_id'
    #     res = {}
    #     #for user in self.browse(cr, uid, ids, context=context):
    #     activity_id= self.pool.get('crm.lead.activity').browse(cr, uid, ids, context=context)
    #     print 'user_id', activity_id
    #
    #     user_id= self.browse(cr, uid, activity_id, context=context).create_uid
    #     print 'user_id', user_id
    #         # section_ids = self.pool.get('crm.case.section').search(cr, uid, [('member_ids', '=', user_id)],context=context)
    #         # if not section_ids:
    #         #     print 'nooooooooo'
    #         #     res[user.id] = 0
    #         # else:
    #         #     print 'section_ids', section_ids
    #         #     coach_id = self.pool.get('crm.case.section').browse(cr, uid, section_ids[0], context=context).user_id.id
    #         #     print 'coach_id', coach_id
    #         #     res[user.id] = coach_id
    #     return True

    _columns = {
        'name':fields.char('Titre'),
        'partner_id': fields.many2one('res.partner','Partenaire',required =True),
        'date_deadline': fields.date(string='Date de fin',
                                     help="Estimate of the date on which the opportunity will be won."),
        'date_action': fields.date(string='Date début', select=True),
        'title_action': fields.char(string='Titre de prochaine action'),
        'priority': fields.selection([
            ('0', 'Very Low'),
            ('1', 'Low'),
            ('2', 'Normal'),
            ('3', 'High'),
            ('4', 'Very High')], 'Priorité'),

        'type': fields.selection([
            ('Mail', "Email"),
            ('Appel', "Appel"),
	    ('Reunion',"Réunion"),

        ], 'Type'),
	    # 'coach_id': fields.function(_get_coach_id, type="integer"),

    }







