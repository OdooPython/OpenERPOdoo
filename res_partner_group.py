# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import date
import time



class res_partner_group(models.Model):
	_name = "res.partner.group"

	name = fields.Char(string="Nom du groupe")
	code = fields.Char(string="Abréviation")
	partner_ids = fields.Many2many(comodel_name="res.partner", relation="group_partner_rel", column1="group_id", column2="partner_id", string="Opérateurs économiques")
