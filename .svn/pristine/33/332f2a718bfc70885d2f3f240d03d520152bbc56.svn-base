# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime

class wizard_question(osv.osv_memory):
    _name = "wizard.question"
    _description = "liste question"

    _columns = {
        'survey_id': fields.many2one('survey.survey', 'Sondage', required=True),
        # 'page_ids': fields.many2one('survey.page', 'Page', required=True),

        #'date_from': fields.date('Date ', required=True, select=True),

    }
    
    def create_report(self, cr, uid, ids, context={}):
        data = self.read(cr,uid,ids,)[-1]
        print data,' create_report('
	res={}
	res={
            'type'         : 'ir.actions.report.xml',
            'report_name'   : 'jasper_qestion_print',
            'datas': {
                    'model':'survey.question',
                    'question': context.get('question') and context.get('question')[0] or False,
                    'reponse': context.get('labels_ids') and context.get('labels_ids') or [],
                    'form':data
                    },
            'nodestroy': False
        }
        return res

  
wizard_question()
