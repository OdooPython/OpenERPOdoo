# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import urllib2
import urllib, json
import simplejson
import requests
from six.moves.urllib.request import urlopen
from random import randint

class cci_crm_infocham(osv.Model):
    _name = 'cci.crm.infocham'

    _columns = {
	'url':fields.char('URL'),
	'code_cci':fields.integer('Code CCI'),
	}

    def get_operateur(self, cr, uid, ids, context=None):
	code_cci=self.browse(cr,uid,ids,context=context).code_cci
	get_url= self.browse(cr,uid,ids,context=context).url
	#url="http://196.203.88.123:806/ws/adhesion/cci/"+str(code_cci)
	url=get_url+"/ws/adhesion/cci/"+str(code_cci)
	r = requests.get(url)
	r.encoding = 'utf-8'
	list_raison_sociale=[]
	list_adhesion=[]
	try:
	    foo = json.loads(r.text, 'utf-8')

	    #récuperer les modules 
	    res_partner = self.pool.get('res.partner')
	    product_temp = self.pool.get('product.template')
	    partner_category = self.pool.get('res_partner_category')
	    
	    #créer une référence aéatoire pour l'adhésion
	    ref=randint(1, 100)


            for partner in foo:	
	        #recuperer les trois listes
		adhesions_list = partner['adhesion']
		inscription_list = partner['inscription']
		personnes_list = partner['personnes']


		nom = inscription_list.get('nom')
		prenom = inscription_list.get('prenom')
		secteur_activite = inscription_list.get('secteur_activite')
		matricule_fisc = inscription_list.get('matricule_fisc')
		web_siege = inscription_list.get('web_siege')
		email_siege = inscription_list.get('email_siege')
		adresse = inscription_list.get('adresse')
		code_postale = inscription_list.get('code_postale')
		localite = inscription_list.get('localite')
		gouvernorat = inscription_list.get('gouvernorat')
		telephone = inscription_list.get('telephone')
		raison_sociale = inscription_list.get('raison_sociale')


		category_ids=self.pool.get('res.partner.category').search(cr,uid,[('name', '=',secteur_activite)])
		category_id=self.pool.get('res.partner.category').browse(cr,uid,category_ids).id


		#contact premier responsable 
		email = inscription_list.get('email')
		nom_resp = inscription_list.get('nom_premier_resp')
		prenom_resp = inscription_list.get('prenom_premier_resp')
		fonction = inscription_list.get('type_operateur')


		cr.execute('SELECT name, id, email, membership_state FROM res_partner')
		lines_partner = cr.dictfetchall()

		for line in lines_partner:
			partner_membership_id = line['id']
			name = line['name']
			list_raison_sociale.append(name)

		#les valeurs à ajouter
		vals_op = {
			'name': raison_sociale,
			'website': web_siege,
			'email': email_siege,
			'street': adresse,
			'zip': code_postale,
			'city': gouvernorat,
			'phone': telephone,
			#'category_id': category_id,
			'is_company': True,
			'matricule_fiscale':matricule_fisc,
		}


		if raison_sociale in list_raison_sociale:
		#il existe
			part_ids=self.pool.get('res.partner').search(cr,uid,[('name', '=',raison_sociale)])
			part_id=self.pool.get('res.partner').browse(cr,uid,part_ids).id
			membership_state = self.pool.get('res.partner').browse(cr,uid,part_id).membership_state
			update_partner_id=res_partner.write(cr,uid,part_id,vals_op,context=context)
			cr.execute("DELETE FROM res_partner_res_partner_category_rel WHERE category_id =%s AND partner_id =%s",(category_id,part_id))
			cr.execute("INSERT INTO res_partner_res_partner_category_rel (partner_id , category_id) VALUES (%s, %s)",(part_id, category_id))
			type_adh =adhesions_list.get('type')
			montant_adhesion = adhesions_list.get('montant_adhesion')
			date_adhesion = adhesions_list.get('date_adhesion')


			#les valeurs à ajouter dans product_template dont le type=service
			vals_adh = {
				'name':type_adh,
				'list_price':montant_adhesion,
				'type':'service',
				'membership':True,
				'membership_date_from':date_adhesion,
				'default_code': 'ad'+str(ref),
			}

			#récuperer les informations à comparer a propos l'adhesion
			cr.execute('SELECT name FROM product_template WHERE type=%s',('service',))
			lines_product = cr.dictfetchall()
			for adhesion in lines_product:
		    		name_adhesion = adhesion['name']
				list_adhesion.append(name_adhesion)


			if type_adh in list_adhesion:
				#search(cr, uid, [('name', '=', name)])
				#browse(cr, uid,id)
				adh_ids=self.pool.get('product.template').search(cr,uid,[('name', '=',type_adh)])
				adh_id=self.pool.get('product.template').browse(cr,uid,adh_ids).id

				product=self.pool.get('product.product').search(cr,uid,[('product_tmpl_id','=',adh_id)])
				product_id=self.pool.get('product.product').browse(cr,uid,product).id
			
				update_adhesion_id=product_temp.write(cr,uid,adh_id,vals_adh,context=context)
			else :
				adhesion_id=product_temp.create(cr,uid,vals_adh,context=context)

			#vérifier s'il a une adhésion sinon ajouter son adhesion 
			if membership_state  == 'none' :
				cr.execute("INSERT INTO membership_membership_line (state, member_price , membership_id, partner, date_from) VALUES (%s, %s ,%s ,%s ,%s)",('paid', montant_adhesion, product_id, partner_membership_id, date_adhesion))
				
			elif membership_state == 'paid':
				print "............."
					
		else :
		#n'existe pas
			partner_id=res_partner.create(cr,uid,vals_op,context=context)
			cr.execute("DELETE FROM res_partner_res_partner_category_rel WHERE category_id =%s AND partner_id =%s",(category_id,partner_id))
			cr.execute("INSERT INTO res_partner_res_partner_category_rel (partner_id , category_id) VALUES (%s, %s)",(partner_id, category_id))

			#test des contact responsable et personnes 
			name_resp=nom_resp +" "+ prenom_resp
			vals_reponsable = {
				'name': name_resp,
				'email': email,
				'street': adresse,
				'zip': code_postale,
				'city': gouvernorat,
				'mobile': telephone,
				'function':fonction,
				'is_company': False,
				'parent_id': partner_id,
				'matricule_fiscale':matricule_fisc,
			}
			responsable_id=res_partner.create(cr,uid,vals_reponsable,context=context)
			if personnes_list :
				for personne in personnes_list :
					first_name = personne.get('first_name')
					last_name = personne.get('last_name')
					mail = personne.get('mail')
					phone = personne.get('phone')
					qualification = personne.get('qualification')

					name_personne=first_name+" "+last_name
					vals_personnes = {
						'name': name_personne,
						'email': mail,
						'street': adresse,
						'zip': code_postale,
						'city': gouvernorat,
						'mobile': phone,
						'function':qualification,
						'is_company': False,
						'parent_id': partner_id,
					}
					personne_id=res_partner.create(cr,uid,vals_personnes,context=context)

			else :
				#traitement des personnes
				cr.execute('SELECT name FROM product_template WHERE type=%s',('service',))
				lines_product = cr.dictfetchall()
				for adhesion in lines_product:
			    		name_adhesion = adhesion['name']
					list_adhesion.append(name_adhesion)


				if type_adh in list_adhesion:
					#search(cr, uid, [('name', '=', name)])
					#browse(cr, uid,id)
					adh_ids=self.pool.get('product.template').search(cr,uid,[('name', '=',type_adh)])
					adh_id=self.pool.get('product.template').browse(cr,uid,adh_ids).id

					product=self.pool.get('product.product').search(cr,uid,[('product_tmpl_id','=',adh_id)])
					product_id=self.pool.get('product.product').browse(cr,uid,product).id
			
					update_adhesion_id=product_temp.write(cr,uid,adh_id,vals_adh,context=context)
				else :
					adhesion_id=product_temp.create(cr,uid,vals_adh,context=context)

				#vérifier s'il a une adhésion sinon ajouter son adhesion 
				if membership_state  == 'none' :
					cr.execute("INSERT INTO membership_membership_line (state, member_price , membership_id, partner, date_from) VALUES (%s, %s ,%s ,%s ,%s)",('paid', montant_adhesion, product_id, partner_membership_id, date_adhesion))
				
				elif membership_state == 'paid':
					print "..................."
		#The method get() returns a value for the given key. If key is not available then returns default value None.
		#recuperer les données des adhesions 
			
			
	except Exception, e:
	    print "Why didn't i get a json ? Maybe it wasn't a json..."
	    print "What is it then? It seems is a {0} whose length is {1}".format(
		r.text.__class__, len(r.text)
	    )
	#raise osv.except_osv(('CONNECTEUR CRM INFOCHAM'),('Connexion établie entre INFOCHAM et CRM'))

	#return_id=self.pool.get('warning_box').info('CONNECTEUR CRM INFOCHAM', 'Connexion établie entre INFOCHAM et CRM!')
	return True
#
