# -*- coding: utf-8 -*-
from openerp.tools.translate import _
from openerp.osv import fields, osv
from openerp.exceptions import Warning

class survey_survey(osv.Model):
    _name = 'survey.survey'
    _inherit ='survey.survey'

    _columns = {
	'product_id' :fields.many2one('product.template', string="Produit", required=True),
    }

class survey_page(osv.Model):
    _name = 'survey.page'
    _inherit ='survey.page'

class survey_question(osv.Model):
    _name = 'survey.question'
    _inherit ='survey.question'


class survey_label(osv.Model):
    _name = 'survey.label'
    _inherit ='survey.label'

# class survey_mail_compose_message(osv.TransientModel):
#     _name = 'survey.mail.compose.message'
#     _inherit = 'survey.mail.compose.message'
