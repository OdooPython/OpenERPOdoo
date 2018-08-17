# -*- coding: utf-8 -*-

from openerp import models, fields, api

class cci_consultation(models.Model):
	_name = 'cci.consultation'

    	name =fields.Char(string="Réference",readonly=True, default=lambda self:self.env['ir.sequence'].get('RefConsult'))
	type_id = fields.Many2one('cci.type.consultation', 'Type de consultation' , required=True)
	date_cons = fields.Date(string='Date', default=fields.Date.today(), )

	op_eco_exist = fields.Boolean(string="Operateur economique existe", )

	op_eco_id = fields.Many2one(comodel_name="res.partner", string="Operateur economique", )
	op_eco_new = fields.Char(string="Nouveau Operateur economique", )

	note =fields.Text(string="Note",)

    #type_conv_ids = fields.Many2one(comodel_name="type.conventions", string="Professionnel santé", )

class cci_type_consultation(models.Model):
	_name = 'cci.type.consultation'
    	name = fields.Char(string="Type", required=True, )
