# -*- coding: utf-8 -*-

from datetime import date, datetime
from dateutil import relativedelta
from openerp import tools, api
from openerp.osv import fields, osv
from openerp.exceptions import Warning
from openerp.exceptions import except_orm

class res_partner(osv.osv):
    _inherit = 'res.partner'

#---------------------------(opportunité en cours,appel en cours,réunion en cours) add by Houssem
    def _phonecall_count(self, cr, uid, ids, field_name, arg, context=None):
	res = {}
	for partner in self.browse(cr, uid, ids, context):
		if partner.is_company:
			operator = 'child_of'
		else:
			operator = '='

		phonecall_ids = self.pool['crm.lead'].search(cr, uid, [('partner_id', operator, partner.id),('type', '=', 'opportunity'),('type_act', '=', 'Appel'),('stage_id.id', '!=', 6),('stage_id.id', '!=', 7),])
		res[partner.id] = len(phonecall_ids)
	return res

    def _opportunity_meeting_phonecall_count(self, cr, uid, ids, field_name, arg, context=None):
	res = dict(map(lambda x: (x, {'opportunity_count': 0, 'meeting_count': 0}), ids))
	# the user may not have access rights for opportunities or meetings
	try:
		for partner in self.browse(cr, uid, ids, context):
			if partner.is_company:
				operator = 'child_of'
			else:
				operator = '='
			opp_ids = self.pool['crm.lead'].search(cr, uid, [('partner_id', operator, partner.id),('type', '=', 'opportunity'),('stage_id.id', '!=', 6),('stage_id.id', '!=', 7),], context=context)
			meeting_ids = self.pool['crm.lead'].search(cr, uid, [('partner_id', operator, partner.id),
('type', '=', 'opportunity'),('type_act', '=', 'Reunion'),('stage_id.id', '!=', 6),('stage_id.id', '!=', 7),])
			res[partner.id] = {
				'opportunity_count': len(opp_ids),
				'meeting_count': len(meeting_ids),
			}
	except:
		pass
	return res

#-------------------total des opportunités gagné pour l'opérateur en cours ajouté par marwa
    def _opportunity_order_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x,0), ids))
	try:
		for partner in self.browse(cr, uid, ids, context):
			if partner.is_company:
				operator = 'child_of'
			else:
				operator = '='

			opport_ids = self.pool['crm.lead'].search(cr, uid, [('partner_id', operator, partner.id),('type', '=','opportunity'),('stage_id.id', '=', 6),])
			res[partner.id] = len(opport_ids)
	except:
		pass
	return res


#---------------------------colonnes
    _columns = {
	'codif_infocham':fields.integer('Code infocham'),
	'matricule_fiscale' : fields.char("Matricule fiscale"),
	'code_tva' : fields.char("Code TVA"),
	#add by Houssem se trouve dans crm/res.partner 
	#update by marwa
	'opportunity_count': fields.function(_opportunity_meeting_phonecall_count, string="Opportunités en cours", type='integer', multi='opp_meet'),

	'meeting_count': fields.function(_opportunity_meeting_phonecall_count, string="Rendez-vous planifiés", type='integer',multi='opp_meet'),

	'phonecall_count': fields.function(_phonecall_count, string="Appels planifiés", type="integer"),

        'opportunity_order_count': fields.function(_opportunity_order_count, string='# of Sales Order', type='integer'),

	#un opérateur peut avoir un ou pluesieurs produits
	'fiche_product_ids':fields.many2many('product','fiche_product_operateur_rel',string="Liste des produits"),
}

#---------------------------classe définit pour es droits d'accès
class res_users(osv.osv):
    _inherit = 'res.users'


class res_partner_category(osv.Model):
    _inherit = 'res.partner.category'

