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
import tempfile
import base64



class operator_opportunity(models.Model):
    _name = 'cci.document.alfresco.operator'

    node = fields.Char(required=True)
    nom_fichier = fields.Char(required=True)
    description = fields.Text()
    operator_id = fields.Many2one('res.partner',ondelete='cascade')

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



class res_partner(models.Model):
    _name='res.partner'
    _inherit = 'res.partner'

    document_ids = fields.One2many('cci.document.alfresco.operator', 'operator_id', string='Operateurs economiques')



    @api.multi
    def ajout(self):
        return {
            'name': "Les documents des opérateurs économiques",
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cci.document.alfresco.operator.wizard',
            'view_id ref="wizard_form_view_oper"': True,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
