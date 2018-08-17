# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _
import time
from datetime import datetime,date

class wizard_report_options(osv.Model):
    _name = "cci.wizard.option"
    _description = "Report option Wizard"

    _columns = {
        'partner_ids': fields.many2many('res.partner', 'partner_wiz_rel', 'report_id', 'partner_id', 'Liste des opérateurs économiques', required=True),
        'section_ids': fields.many2many('crm.case.section','section_wiz_rel', 'report_id', 'section_id', 'Liste des départements'),
        'secteur_ids': fields.many2many('res.partner.category', 'secteur_wiz_rel', 'report_id','secteur_id', "Liste des secteurs d'activités"),
        'user_ids': fields.many2many('res.users', 'user_wiz_rel', 'report_id', 'user_id', 'Liste des utilisateurs'),
        'date_debut':fields.date(required=True),
        'date_fin':fields.date(required=True),
        'operateur':fields.boolean("Opérateur économique"),
        'commercial':fields.boolean("Commercial"),




    }


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
        return {'type': 'ir.actions.report.xml', 'report_name': 'jasper_options_print', 'datas': datas}


wizard_report_options()

