# -*- coding: utf-8 -*-
import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')

import tempfile
import base64
from openerp import models, fields, api
from cmislib import CmisClient, Repository, Folder


class DocumentEmails(models.Model):

    _name = 'cci.document.alfresco.emails'

    node = fields.Char(required=True)
    nom_fichier = fields.Char(required=True)
    description = fields.Text()
    email_id = fields.Many2one('mail.mail',ondelete='cascade')

    @api.multi
    def unlink(self):
        repo = self.env['cci.alfresco.configuration'].connection_alfresco()
        try:
            doc = repo.getObject(self.node)
            doc.delete()
        except:
            pass
        finally:
            models.Model.unlink(self)


    @api.multi
    def download_document(self):
        repo = self.env['cci.alfresco.configuration'].connection_alfresco()

        doc = repo.getObject(self.node)
        doc_content = doc.getContentStream()

        file_obj = tempfile.NamedTemporaryFile(delete=False)
        file_name = file_obj.name
        file_obj.write(doc_content.read())
        file_obj.close()

        file_base64 = ''
        with open(file_name, "rb") as file:
            file_base64 = base64.encodestring(file.read())

        download_wizard_record = self.env['cci.download.wizard'].create({'download_link' :file_base64 ,'nom_fichier':self.nom_fichier})

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cci.download.wizard',
            'res_id': int(download_wizard_record),
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


class MailMail(models.Model):
    _name ='mail.mail'
    _inherit = 'mail.mail'

    document_emails_ids = fields.One2many('cci.document.alfresco.emails', 'email_id', string='Documents')
    document_produit_ids = fields.Many2many('cci.document.alfresco.produit', string="Les documents des produits",ondelete='cascade')


    # @api.onchange('opportunity_ids')
    # def onchange_contact(self):
    #     res = {}
    #     res['domain'] = {'document_produit_ids': [('produit_id', '=', 'opportunity_ids.product_id.id')]}
    #     return res

    # def onchange_opportunity_ids(self, cr, uid, ids, participant_id, context=None):
    #     res = {}
    #     name = self.pool.get('product.participant').browse(cr, uid, participant_id, context=context).name.id
    #     res['domain'] = {'name': [('parent_id', '=', name)]}
    #     return res

    @api.onchange('opportunity_ids')
    def onchange_opportunity_ids(self):
            return {'domain': {'document_produit_ids': [('produit_id', '=', self.opportunity_ids.product_id.id)]}}



    @api.multi
    def _get_id_oppor(self, context=None):
        return context.get('opportunity_ids', False)

    @api.multi
    def _get_nom_op_eco(self, context=None):
        id_op_eco = context.get('recipient_ids', False)
        nom_op_eco = self.env['res.partner'].browse(id_op_eco).name
        return nom_op_eco

    @api.multi
    def _get_active_id(self, context=None):
        return context.get('active_id', False)


    @api.multi
    def ajout(self):
        return {
            'name':"Les documents des emails",
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cci.document.alfresco.emails.wizard',
            'view_id ref="wizard_email_doc_form_view"': True,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
