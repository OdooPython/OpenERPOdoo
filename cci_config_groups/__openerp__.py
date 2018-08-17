# -*- coding: utf-8 -*-
{
    'name': "CCI CONFIGURATION GROUPES",
    'version': "0.1",
    'description': """
CCI CONFIGURATION GROUPES.
========================
Ce module offre la gestion des groupes, pour nous permettre de gérer les droits d'accès de l’application.
CCI défini trois groupes :\n
	\n* Groupe "Administrateurs" qui contiennent les administrateurs de l’application. 
	\n* Groupe "Responsables Département" qui contient les chefs des départements.
	\n* Groupe "Membres Département" qui contient les commerciaux des départements. """,

    "author": "Marwa BEN MESSAOUD I-WAY",
    "website" : "http://www.iway-tn.com",
    'category': "Groups",
    'depends': ['crm','sale'],
    'data': ['views/cci_menu_crm_view.xml',
            'views/ir_mail_server_views.xml',
            'security/cci_security.xml',
            'security/ir.model.access.csv',
],
    'installable': True,
    'auto_install': False,
    'application': False,

}
