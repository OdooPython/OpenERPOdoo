# -*- coding: utf-8 -*-
import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')
import matplotlib.pyplot as plt


from openerp import models, fields, api


from cmislib import CmisClient, Repository, Folder
from cmislib.exceptions import CmisException


class Document_ope_eco(models.Model):
    _name = 'cci.document.oper.eco'

    node = fields.Char(required=True)
    nom_fichier = fields.Char(required=True)
    description = fields.Text()

    ope_eco_id = fields.Many2one('mail.information',ondelete='cascade')

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
# update by salwa ksila le 03/07/2017

class mail_information(models.Model):
    _name='mail.information'
    _inherit = 'mail.information'

    document_ids = fields.One2many('cci.document.oper.eco', 'ope_eco_id', string='Documents')


    #  update by salwa ksila 23/07/2017
    @api.multi
    def ajout_op_eco(self):
        return {
            'name': "Les documents des emails pour les opérateurs économiques",
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cci.document.ope.eco.wizard',
            'view_id ref="wizard_form_view4"': True,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
