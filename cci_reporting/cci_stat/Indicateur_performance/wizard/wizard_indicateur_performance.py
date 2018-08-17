# -*- encoding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.exceptions import ValidationError
from openerp.tools.translate import _
import time
from datetime import datetime,date

class wizard_performance(osv.osv_memory):
	_name = "cci.wizard.performdep"
	_columns = {
		'date1':fields.date(required=True),
		'date2':fields.date(required=True),
		'departement_id':fields.many2one('crm.case.section',required=True)
	}

	def _check_period(self, cr, uid, ids, context=None):
		for val in self.read(cr, uid, ids, ['date1','date2'], context=context):
			if val['date2'] < val['date1']:
				return False
		return True

	_constraints = [
		(_check_period, u'Erreur: La deuxième date doit être supèrieure à la première', ['date2'])
	]


	def create_report(self, cr, uid, ids, context=None):
		datas = {}
		if context is None:
			context = {}
		data = self.read(cr, uid, ids)[0]
		datas = {
			'ids': [],
			'model': 'object.object',
			'form': data
		}
		return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_perform_dep_print', 'datas': datas}


wizard_performance()

