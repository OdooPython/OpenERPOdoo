# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class ir_mail_server(osv.osv):
	_inherit = "ir.mail_server"
	_columns = {
		'user_id': fields.many2one('res.users', string="Propriétaire"),
	}