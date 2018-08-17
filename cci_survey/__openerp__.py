# -*- coding: utf-8 -*-
{
    "name": "CCI SONDAGE",
    "description":  """
CCI SONDAGE.
========================
Ce module crée des sondages sur un produit en question, pour les envoyer aux opérateurs économiques.
Ce module offre aux opérateurs économiques de donner ses avis sur les produits offerts par CCI   
""",
    "author": "Maroua TURKI I-Way",
    "website": "http://www.i-way.tn.com",
    "category": 'Sondage',
    "version": '0.1',
    "depends": ['base','survey','product'],

    # always loaded
    "data": [
	'security/ir.model.access.csv',
    	'survey_view.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo.xml',
   #],
}
