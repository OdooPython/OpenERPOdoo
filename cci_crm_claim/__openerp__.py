# -*- coding: utf-8 -*-
{
    "name": "CCI CRM CLAIMS",
    "summary": "",
    "description": "",
    "author": "Maroua TURKI & Marwa BEN MESSAOUD I-Way",
    'description': """
CCI CRM CLAIMS.
========================
Ce module offre la gestion des réclamations sur le produit en question. 
""",

    "website": "http://www.i-way.tn.com",
    "category": 'Claim',
    "version": '0.1',
    "depends": ['base','hr','sale','crm_claim'],

    # always loaded
    "data": [
	'security/ir.model.access.csv',
    #'crm_claim_data.xml',
    'crm_claim_view.xml',
    'crm_claim_workflow.xml'
    ],
    # only loaded in demonstration mode
    #'demo': [
    #    'demo.xml',
   #],
}
