# -*- coding: utf-8 -*-
from openerp import models, fields, api
import tempfile
import base64
import os


class Wizard(models.TransientModel):
    _name = 'cci.document.alfresco.reunion.wizard'
    chemin = fields.Binary(string="Chemin")
    nom_fichier = fields.Char(string="Nom du fichier", required="True", readonly=False)
    description = fields.Text(string ="Description")

    @api.multi
    def _get_active_id(self ,context=None):
        return context.get('active_id', False)

    @api.multi
    def _get_cin(self ,context=None):
        return context.get('name', False)

    @api.multi
    def _get_title(self, context=None):
        return context.get('name', False)

#update by salwa ksila le 03/07/2017
    @api.multi
    def upload_document(self):
        repo = self.env['cci.alfresco.configuration'].connection_alfresco()
        root = repo.rootFolder

        try:
            crm = repo.getObjectByPath('/CRM')
        except:
            crm = root.createFolder('CRM')
        try:
            Reunions = repo.getObjectByPath('/CRM/Reunions')
        except:
            Reunions = crm.createFolder('Reunions')
        try:
            sFolder = repo.getObjectByPath( '/CRM/Reunions/' +self._get_cin(self.env.context))

        except:
            sFolder = Reunions.createFolder(self._get_cin(self.env.context))


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


        record = self.env['cci.document.alfresco.reunion'].create({'node' :document.id ,'nom_fichier':
            self.nom_fichier ,'description' :self.description ,'reunion_id' :self._get_active_id(self.env.context) ,})



