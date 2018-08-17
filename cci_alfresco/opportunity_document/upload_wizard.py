# -*- coding: utf-8 -*-
from openerp import models, fields, api
import tempfile
import base64
import os


class Wizard(models.TransientModel):
	_name = 'cci.document.alfresco.opportunity.wizard'
	chemin = fields.Binary(string="Chemin")
	# nom_fichier = fields.Char(string="Nom du fichier" ,compute="_onchange_chemin" ,readonly=False)
	nom_fichier = fields.Char(string="Nom du fichier", required="True", readonly=False)
	description = fields.Text(string="Description")

	@api.multi
	def _get_active_id(self, context=None):
		return context.get('active_id', False)

	@api.multi
	def _get_product_name(self, context=None):
		product_id = context.get('product_id', False)
		product_name = self.env['product.template'].browse(product_id).name
		return product_name

	@api.multi
	def _get_partner_name(self, context=None):
		partner_id = context.get('partner_id', False)
		partner_name = self.env['res.partner'].browse(partner_id).name
		return partner_name

	@api.multi
	def upload_document(self):
		repo = self.env['cci.alfresco.configuration'].connection_alfresco()
		root = repo.rootFolder

		try:
			crm = repo.getObjectByPath('/CRM')
		except:
			crm = root.createFolder('CRM')
		try:
			dossier_opportunites = repo.getObjectByPath("/CRM/Opportunites")
		except:
			dossier_opportunites = crm.createFolder('Opportunites')

		try:
			dossier_produit = repo.getObjectByPath("/CRM/Opportunites/" + self._get_product_name(self.env.context))
		except:
			dossier_produit = dossier_opportunites.createFolder(self._get_product_name(self.env.context))

		try:
			dossier_op_eco = repo.getObjectByPath(
				"/CRM/Opportunites/" + self._get_product_name(self.env.context) + '/' + self._get_partner_name(
					self.env.context))
		except:
			dossier_op_eco = dossier_produit.createFolder(self._get_partner_name(self.env.context))

		file_extension = os.path.splitext(self.nom_fichier)[1][1:]
		random_with_4_digits = self.env['cci.alfresco.configuration'].random_with_N_digits(4)

		# added by salwa ksila 23/07/2017
		file_data = base64.decodestring(self.chemin)
		file_obj = tempfile.NamedTemporaryFile(delete=False)
		file_name = file_obj.name
		file_obj.write(file_data)
		file_obj.close()

		file_content = open(file_name, 'r')
		document = dossier_op_eco.createDocument(self.nom_fichier[:self.nom_fichier.rindex(file_extension) - 1] + '_' + str(
			random_with_4_digits) + '.' + file_extension, contentFile=file_content)

		self.env['cci.document.alfresco.opportunity'].create({'node': document.id, 'nom_fichier':
				self.nom_fichier, 'description': self.description,
			 'opportunity_id': self._get_active_id(self.env.context), })


