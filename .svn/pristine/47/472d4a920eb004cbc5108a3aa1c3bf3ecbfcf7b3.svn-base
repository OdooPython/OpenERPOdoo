# -*- coding: utf-8 -*-


from openerp import models, fields, api
import tempfile
import base64
import os



class Wizard(models.TransientModel):
    _name = 'cci.document.alfresco.emails.wizard'
    chemin = fields.Binary()
    # nom_fichier = fields.Char(string="Nom du fichier" ,compute="_onchange_chemin" ,readonly=False)
    nom_fichier = fields.Char(string="Nom du fichier", required="True", readonly=False)
    description = fields.Text(string ="Description")

    @api.multi
    def _get_active_id(self ,context=None):
        return context.get('active_id', False)

    @api.multi
    def _get_cin(self ,context=None):
        return context.get('subject', False)


    @api.multi
    def upload_document(self):
        repo = self.env['cci.alfresco.configuration'].connection_alfresco()
        root = repo.rootFolder

        try:
            crm = repo.getObjectByPath('/CRM')
        except:
            crm = root.createFolder('CRM')

        try:
            Emails = repo.getObjectByPath('/CRM/Emails')
        except:
            Emails = crm.createFolder('Emails')

        try:
            sFolder = repo.getObjectByPath('/CRM/Emails/Emails Operateurs economiques')
        except:
            sFolder = Emails.createFolder('Emails Operateurs economiques')

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


        self.env['cci.document.alfresco.emails'].create({'node' :document.id ,'nom_fichier':
            self.nom_fichier ,'description' :self.description ,'email_id' :self._get_active_id(self.env.context),})


