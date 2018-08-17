
# -*- coding: utf-8 -*-
{
    'name': "CCI CRM INFOCHAM",
    'version': "0.1",
    "summary": "",
    "description": "Paramétrage CRM avec INFOCHAM",
    "author": "Marwa BEN MESSAOUD I-WAY",
    "category": "CRM Configuration",
    'description': """
CCI CRM INFOCHAM.
========================
Ce module est important. c'est le connecteur entre CCI et INFOCHAM. 
À travers le code du CCI souhaité, tous les opérateurs, et ses adhésions s'ajoutent dans CRM. 
""",
    "website" : "http://www.iway-tn.com",
    'depends': ['crm','sale'],
    'data': ['cci_crm_infocham_view.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,

}
