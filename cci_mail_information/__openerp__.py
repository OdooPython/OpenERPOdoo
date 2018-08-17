# -*- coding: utf-8 -*-
{
    "name": "CCI LETTRE D'INFORMATION",
    "description": """
CCI LETTRE D'INFORMATION.
========================
Ce module offre l'envoi des lettres d'informations aux adhérants et aux non adhérants.
Aussi il choisit les destinataires suivant trois critères:\n
	\n* Tous les opérateurs économiques qui ont commandé un produit particulier,
	\n* Tous les adhérants,
	\n* Tous les opérateurs économiques qui appartient à un ou plusieurs secteurs d'activités,
""",
    "author": "Maroua TURKI & Houssem ABID & Marwa BEN MESSAOUD I-Way",
    "website": "http://www.i-way.tn.com",
    "category": 'Lettre Information',
    "version": '0.1',
    "depends": ['base', 'base_setup','mail'],

    # always loaded
    "data": [
	'security/ir.model.access.csv',
        'mail_information_view.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo.xml',
   #],
}
