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


class Document_email_non_adh(models.Model):
    _name = 'cci.document.non.adherent'

    node = fields.Char(required=True)
    nom_fichier = fields.Char(required=True)
    description = fields.Text()

    non_adh_id = fields.Many2one('mail.information',ondelete='cascade')

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

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cci.download.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

# update by salwa ksila le 03/07/2017

class mail_information(models.Model):
    _name='mail.information'
    _inherit = 'mail.information'

    document_non_adh_ids = fields.One2many('cci.document.non.adherent', 'non_adh_id', string='Documents')


    #update by salwa ksila  25/07/2017
    @api.multi
    def ajout(self):
        return {
            'name': "Les documents des emails pour les non adhérents",
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'cci.document.non.adherent.wizard',
            'view_id ref="wizard_form_view3"': True,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
