# -*- coding: utf-8 -*-
from openerp import models, fields, api
import tempfile
import base64
import os


class Wizard(models.TransientModel):
    _name = 'cci.document.non.adherent.wizard'
    chemin = fields.Binary(string="Chemin")
    # nom_fichier = fields.Char(string="Nom du fichier" ,compute="_onchange_chemin" ,readonly=False)
    nom_fichier = fields.Char(string="Nom de fichier", required="True", readonly=False)
    description = fields.Text(string ="Description")

    @api.multi
    def _get_active_id(self ,context=None):
        return context.get('active_id', False)

    @api.multi
    def _get_cin(self ,context=None):
        return context.get('subject', False)

    @api.multi
    def _get_title(self, context=None):
        return context.get('type_menu', False)

    # update by salwa ksila le 23/07/2017
    @api.multi
    def upload_document_non_adh(self):
        repo = self.env['cci.alfresco.configuration'].connection_alfresco()
        root = repo.rootFolder

        try:
            crm = repo.getObjectByPath('/CRM')
        except:
            crm = root.createFolder('CRM')

        try:
            Emails_NAD = repo.getObjectByPath('/CRM/Emails')
        except:
            Emails_NAD = crm.createFolder('Emails')


        try:
            sFolder = repo.getObjectByPath('/CRM/Emails/Lettre Information Non Adhérents')
        except:
            sFolder = Emails_NAD.createFolder(u'Lettre Information Non Adhérents')


        file_extension = os.path.splitext(self.nom_fichier)[1][1:]
        random_with_4_digits = self.env['cci.alfresco.configuration'].random_with_N_digits(4)

        # added by salwa ksila 23/07/2017
        file_data = base64.decodestring(self.chemin)
        file_obj = tempfile.NamedTemporaryFile(delete=False)
        file_name = file_obj.name
        file_obj.write(file_data)
        file_obj.close()

        file_content = open(file_name, 'r')
        document = sFolder.createDocument(self.nom_fichier[:self.nom_fichier.rindex(file_extension) - 1] + '_' + str(
            random_with_4_digits) + '.' + file_extension, contentFile=file_content)

        record = self.env['cci.document.non.adherent'].create({'node': document.id, 'nom_fichier':
            self.nom_fichier, 'description': self.description, 'non_adh_id': self._get_active_id(self.env.context), })



