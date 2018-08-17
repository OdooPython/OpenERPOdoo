# -*- coding: utf-8 -*-
from datetime import date, datetime
from dateutil import relativedelta
from openerp import tools
from openerp.osv import fields, osv



class crm_case_section(osv.osv):
    _name = "crm.case.section"
    _inherit = "crm.case.section"
    #Update by marwa 25-10-2017
    _columns = {
	'parent_id': fields.many2one('crm.case.section', 'Parent Team'),
        #liste des categories
	'categories_ids': fields.many2many('product.category',string="Catégorie"),
	'user_id': fields.many2one('res.users', 'Chef de département'),
}


