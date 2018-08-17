# -*- coding: utf-8 -*-
from openerp import models, fields, api
import tempfile
import base64
import os
import time,datetime


class Wizard(models.TransientModel):
    _name = 'cci.document.alfresco.message.wizard'
    chemin = fields.Binary(string="Chemin")
    # nom_fichier = fields.Char(string="Nom du fichier" ,compute="_onchange_chemin" ,readonly=False)
    nom_fichier = fields.Char(string="Nom du fichier", required="True", readonly=False)
    description = fields.Text(string ="Description")

    @api.multi
    def _get_active_id(self ,context=None):
        return context.get('active_id', False)


    @api.multi
    def upload_document(self):
	#update 10-09-2017
        repo = self.env['cci.alfresco.configuration'].connection_alfresco()

        root = repo.rootFolder

        try:
            crm_folder = repo.getObjectByPath('/CRM')
        except:
            crm_folder = root.createFolder('CRM')

        try:
            Emails_folder = repo.getObjectByPath('/CRM/Emails')
        except:
            Emails_folder = crm_folder.createFolder('Emails')

        try:
            messages_folder = repo.getObjectByPath('/CRM/Emails/Messages personnels')
        except:
            messages_folder = Emails_folder.createFolder('Messages personnels')


        # added by salwa ksila 06/04/2017
        data = base64.decodestring(self.chemin)
        fobj = tempfile.NamedTemporaryFile(delete=False)
        fname = fobj.name
        fobj.write(data)
        fobj.close()
        eContent = open(fname, 'r')
        file_extension = os.path.splitext(self.nom_fichier)[1][1:]

        if file_extension:
            msg_attach_file = messages_folder.createDocument(self.nom_fichier[:self.nom_fichier.rindex(file_extension)-1] + '_'+ str(time.strftime('%d_%m_%Y_%H_%M_%S')) + '.' + file_extension,contentFile=eContent)
        else:
            msg_attach_file = messages_folder.createDocument(self.nom_fichier + '_' + str(time.strftime('%d_%m_%Y_%H_%M_%S')),contentFile=eContent)



        self.env['cci.document.alfresco.message'].create({'node' :msg_attach_file.id ,'nom_fichier':
            self.nom_fichier ,'description' :self.description ,'message_id' :self._get_active_id(self.env.context),})


