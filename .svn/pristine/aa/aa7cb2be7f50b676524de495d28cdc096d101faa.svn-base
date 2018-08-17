# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp import api, tools
from openerp import SUPERUSER_ID
import psycopg2
import time
import tempfile, base64
from openerp.addons.base.ir.ir_mail_server import MailDeliveryException
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _
import base64
import logging
from email.utils import formataddr
from urlparse import urljoin


_logger = logging.getLogger(__name__)

class mail_mail(osv.Model):
	_inherit = "mail.mail"
	_name = 'mail.mail'

	_columns = {
		'opportunity_ids': fields.many2one('crm.lead', 'Opportunite'),#, required=True),
		'partner_contact_id': fields.many2one('res.partner', 'Contact'),# required=True),
		'body_html': fields.html('Rich-text Contents', help="Rich-text/HTML message"),

	}

	# def closed_action_mail(self, cr, uid, ids,context=None):
	# 	mail_id=self.browse(cr, uid, ids,context=context).id
	# 	opportunity_ids=self.browse(cr, uid, ids,context=context).opportunity_ids.id
	# 	return self.pool.get('crm.lead').write(cr, uid, opportunity_ids, {'date_deadline': False,'date_action': False,'title_action': False,'type_act': False})

	def onchange_contact(self, cr, uid, ids, partner_contact_id, context=None):
		courriel = self.pool.get('res.partner').browse(cr, uid, partner_contact_id, context=context).email
		cr.execute('UPDATE mail_mail SET email_to=%s ', (courriel,))
		return {'value': {'email_to': courriel}}

	def create_attachments(self, cr, uid, ids, context=None):
		# ---------récupération des pièces jointes de l'email--------
		active_record = self.browse(cr, uid, ids[0], context=context)
		res = False
		active_record_attachments_ids = []
		active_record_attachments = None

		active_record_attachments_ids = self.pool.get('cci.document.alfresco.emails').search(cr, uid,
																							 [('email_id', "=",
																							   active_record.id)]
																							 , context=context)
		if active_record_attachments_ids:
			active_record_attachments = self.pool.get('cci.document.alfresco.emails').browse(cr, uid, active_record_attachments_ids,
																						 context=context)
		if active_record_attachments:
			repo = self.pool.get('cci.alfresco.configuration').connection_alfresco_old_api(cr, uid, context=context)

			for attach in active_record_attachments:
				doc = repo.getObject(attach.node)
				result = doc.getContentStream()
				fobj = tempfile.NamedTemporaryFile(delete=False)
				fname = fobj.name
				fobj.write(result.read())
				fobj.close()

				with open(fname, "rb") as file:
					file_base64 = base64.encodestring(file.read())
					self.pool.get('ir.attachment').create(cr, uid, {'datas': file_base64, 'datas_fname': attach.nom_fichier,
																	'name': attach.nom_fichier,'res_model':
														  			active_record._name,'res_id': active_record.id}
														  			, context=context)
			res = True
		# --------------------------------------------------------------------------------


		# --------------------Récupération des pièces jointes du poduit------------------------------------

		cr.execute("SELECT cci_document_alfresco_produit_id"
				   " FROM cci_document_alfresco_produit_mail_mail_rel"
				   " WHERE mail_mail_id = " + repr(active_record.id))
		prod_attachments_ids = cr.fetchall()

		if prod_attachments_ids :
			repo = self.pool.get('cci.alfresco.configuration').connection_alfresco_old_api(cr, uid, context=context)
			for prod_attach_id in prod_attachments_ids:
				active_record_product_attachments = self.pool.get('cci.document.alfresco.produit').browse(cr, uid,
																										  prod_attach_id,
																										  context=context)
				for attach in active_record_product_attachments:
					doc = repo.getObject(attach.node)
					result = doc.getContentStream()
					fobj = tempfile.NamedTemporaryFile(delete=False)
					fname = fobj.name
					fobj.write(result.read())
					fobj.close()

					with open(fname, "rb") as file:
						file_base64 = base64.encodestring(file.read())
						self.pool.get('ir.attachment').create(cr, uid, {'datas': file_base64,
																		'datas_fname': attach.nom_fichier,
																		'name': attach.nom_fichier,
																		'res_model':active_record._name,
																		'res_id': active_record.id}, context=context)
			res = True
		return res

	# update by marwa BM le 23-08-2017
	def send_mail(self, cr, uid, ids, auto_commit=False, raise_exception=False, context=None):
		""" Sends the selected emails immediately, ignoring their current
					state (mails that have already been sent should not be passed
					unless they should actually be re-sent).
					Emails successfully delivered are marked as 'sent', and those
					that fail to be deliver are marked as 'exception', and the
					corresponding error mail is output in the server logs.

					:param bool auto_commit: whether to force a commit of the mail status
						after sending each mail (meant only for scheduler processing);
						should never be True during normal transactions (default: False)
					:param bool raise_exception: whether to raise an exception if the
						email sending process has failed
					:return: True
				"""
		context = dict(context or {})
		ir_mail_server = self.pool.get('ir.mail_server')
		ir_attachment = self.pool['ir.attachment']
		attachment_ids = []
		attachments = []

		for mail in self.browse(cr, SUPERUSER_ID, ids, context=context):
			try:
				# TDE note: remove me when model_id field is present on mail.message - done here to avoid doing it multiple times in the sub method
				if mail.model:
					model_id = \
						self.pool['ir.model'].search(cr, SUPERUSER_ID, [('model', '=', mail.model)], context=context)[0]
					model = self.pool['ir.model'].browse(cr, SUPERUSER_ID, model_id, context=context)
				else:
					model = None
				if model:
					context['model_name'] = model.name

				# load attachment binary data with a separate read(), as prefetching all
				# `datas` (binary field) could bloat the browse cache, triggerring
				# soft/hard mem limits with temporary data.
				# -------------------------Choix du serveur SMTP----------------------
				try:
					mail_server_id = self.pool.get('ir.mail_server').search(cr, uid, [('user_id', '=', uid)])[0]

				except:
					mail_server_id = self.pool.get('ir.mail_server').search(cr, uid, [])[0]

				# -------------------------récupération des pièces jointes-------------------
				active_record = self.browse(cr, uid, ids[0], context=context)

				res = self.create_attachments(cr, uid, ids, context=None)
				if res:
					attachment_ids = self.pool.get('ir.attachment').search(cr, uid, [('res_id', "=", active_record.id),
																					 ('res_model', 'like',
																					  active_record._name)],
																		   context=context)
					attachments = [(a['datas_fname'], base64.b64decode(a['datas']))
								   for a in ir_attachment.read(cr, SUPERUSER_ID, attachment_ids,
															   ['datas_fname', 'datas'])]
				else:
					pass

				# ----------------------------------------------------------------------------
				# specific behavior to customize the send email for notified partners
				email_list = []
				if mail.email_to:
					email_list.append(self.send_get_email_dict(cr, uid, mail, context=context))
				for partner in mail.recipient_ids:
					email_list.append(self.send_get_email_dict(cr, uid, mail, partner=partner, context=context))
				# headers
				headers = {}
				bounce_alias = self.pool['ir.config_parameter'].get_param(cr, uid, "mail.bounce.alias", context=context)
				catchall_domain = self.pool['ir.config_parameter'].get_param(cr, uid, "mail.catchall.domain",
																			 context=context)
				if bounce_alias and catchall_domain:
					if mail.model and mail.res_id:
						headers['Return-Path'] = '%s-%d-%s-%d@%s' % (
							bounce_alias, mail.id, mail.model, mail.res_id, catchall_domain)
					else:
						headers['Return-Path'] = '%s-%d@%s' % (bounce_alias, mail.id, catchall_domain)
				if mail.headers:
					try:
						headers.update(eval(mail.headers))
					except Exception:
						pass

				# Writing on the mail object may fail (e.g. lock on user) which
				# would trigger a rollback *after* actually sending the email.
				# To avoid sending twice the same email, provoke the failure earlier
				mail.write({'state': 'exception'})
				mail_sent = False

				# build an RFC2822 email.message.Message object and send it without queuing
				res = None
				for email in email_list:
					msg = ir_mail_server.build_email(
						email_from=mail.email_from,
						email_to=email.get('email_to'),
						subject=email.get('subject'),
						body=email.get('body'),
						body_alternative=email.get('body_alternative'),
						email_cc=tools.email_split(mail.email_cc),
						reply_to=mail.reply_to,
						attachments=attachments,
						message_id=mail.message_id,
						references=mail.references,
						object_id=mail.res_id and ('%s-%s' % (mail.res_id, mail.model)),
						subtype='html',
						subtype_alternative='plain',
						headers=headers)
					try:
						res = ir_mail_server.send_email(cr, uid, msg,
														mail_server_id=mail_server_id,
														context=context)
					except AssertionError as error:
						self.pool.get('ir.attachment').unlink(cr, uid, attachment_ids, context=None)

						if error.message == ir_mail_server.NO_VALID_RECIPIENT:
							# No valid recipient found for this particular
							# mail item -> ignore error to avoid blocking
							# delivery to next recipients, if any. If this is
							# the only recipient, the mail will show as failed.
							_logger.warning("Ignoring invalid recipients for mail.information %s: %s",
											mail.message_id, email.get('email_to'))
						else:
							raise
				if res:
					mail.write({'state': 'sent', 'message_id': res})
					mail_sent = True
				#-----------------------------------------------------
					opportunity_ids = self.browse(cr, uid, ids, context=context).opportunity_ids
					subject = self.browse(cr, uid, ids, context=context).subject
					partner_id = self.pool.get('crm.lead').browse(cr, uid, opportunity_ids.id,
																  context=context).partner_id.id
					date_deadline = self.pool.get('crm.lead').browse(cr, uid, opportunity_ids.id,
																	 context=context).date_deadline
					date_action = self.pool.get('crm.lead').browse(cr, uid, opportunity_ids.id, context=context).date_action
					# partner_name = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context).name

					if date_deadline == False and date_action == False:
						date_deadline = time.strftime('%d-%m-%Y %H:%M')
						date_action = time.strftime('%d-%m-%Y %H:%M')
					else:
						date_deadline = date_deadline
						date_action = date_action

					val = {
						'name': subject,
						'partner_id': partner_id,
						'date_deadline': date_deadline,
						'date_action': date_action,
						'type': 'Mail',
					}

					inv_id = self.pool.get('crm.lead.activity').create(cr, uid, val)
					# rendre les champs vides 22-09-2017
					self.pool.get('crm.lead').write(cr, uid, opportunity_ids.id,
													{'date_deadline': False, 'date_action': False, 'title_action': False,
													 'type_act': False})
				#------------------------------------------------------------------------
				# /!\ can't use mail.state here, as mail.refresh() will cause an error
				# see revid:odo@openerp.com-20120622152536-42b2s28lvdv3odyr in 6.1
				if mail_sent:
					_logger.info('Mail with ID %r and Message-Id %r successfully sent', mail.id, mail.message_id)
				self._postprocess_sent_message(cr, uid, mail, context=context, mail_sent=mail_sent)
			except MemoryError:
				# prevent catching transient MemoryErrors, bubble up to notify user or abort cron job
				# instead of marking the mail as failed
				_logger.exception('MemoryError while processing mail with ID %r and Msg-Id %r. ' \
								  'Consider raising the --limit-memory-hard startup option',
								  mail.id, mail.message_id)
				raise
			except psycopg2.Error:
				# If an error with the database occurs, chances are that the cursor is unusable.
				# This will lead to an `psycopg2.InternalError` being raised when trying to write
				# `state`, shadowing the original exception and forbid a retry on concurrent
				# update. Let's bubble it.
				raise
			except Exception as e:
				_logger.exception('failed sending mail.information %s', mail.id)
				mail.write({'state': 'exception'})
				self._postprocess_sent_message(cr, uid, mail, context=context, mail_sent=False)
				if raise_exception:
					if isinstance(e, AssertionError):
						# get the args of the original error, wrap into a value and throw a MailDeliveryException
						# that is an except_orm, with name and value as arguments
						value = '. '.join(e.args)
						raise MailDeliveryException(_("Mail Delivery Failed"), value)
					raise

			if auto_commit is True:
				cr.commit()

		return True

	_default = {
		'recipient_ids': lambda self, cr, uid, context: context.get('recipient_ids', False),
	}


class mail_message(osv.Model):
	_inherit = 'mail.message'
