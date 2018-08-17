# -*- coding: utf-8 -*-
from openerp import models, fields

from openerp.tools.translate import _
from openerp.exceptions import Warning
from datetime import datetime, date



class type_product(models.Model):
    _name = 'product.type'

    name = fields.Char(string="Type", required=True, )
