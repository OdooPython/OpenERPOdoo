# -*- coding: utf-8 -*-

{
    "name": "CCI CRM",
    "version": "0.1",
    "description": """
CCI CRM.
========================
Ce module est trés important, il offre la gestion des opportunités, et de ses différents types d'activités. Aussi il garde la traçabilité de tous les activités. 
""",
    "author": "Marwa BEN MESSAOUD & Salwa KSILA I-WAY",
    "website": "http://iway-tn.com/",
    "category": "CRM",
    "website" : "http://www.iway-tn.com",
    "depends": ['base','crm','survey','sale','product','crm_helpdesk'],
    "init_xml": [],
    "demo_xml": [],
    "update_xml": [
	   'views/sales_team_view.xml',
	   'views/crm_lead_view.xml',
           'views/next_activity_view.xml',
           'views/previous_action_view.xml',
	   'views/crm_menuitem.xml',
	   'views/mail_mail_view.xml',
	   'views/calendar_view.xml',
	   'views/crm_phonecall_view.xml',
	  'views/res_partner_group_view.xml',
	   'security/ir.model.access.csv',

	   #'security/ir_rules.xml',
    ],
    "installable": True,

}
