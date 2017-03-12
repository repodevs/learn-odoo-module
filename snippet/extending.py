# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.addons import decimal_precision as dp
from openerp.fields import Date as fDate
from datetime import timedelta as td


class LibraryBook(models.Model):
	_inherit = 'library.book'

	@api.model
	@api.returns('self', lambda rec: rec.id)
	def create(self, values):
		if not self.user_has_groups('library.group_library_manager'): # cek jika user tidak punya group manager
			if 'manager_remarks' in values: # jika ada value manager_remarks maka munculkan pesan
				raise exceptions.UserError('You are not allowed to modify manager_remarks')

			return super(LibraryBook, self).create(values)


	@api.multi
	def write(self, values):
		if not self.user_has_groups('library.group_library_manager'): # cek jika user tidak punya group manager
			if 'manager_remarks' in values: # jika ada value manager_remarks maka munculkan pesan
				raise exceptions.UserError('You are not allowed to modify manager_remarks')

			return super(LibraryBook, self).write(values)


	@api.model
	def fields_get(self, allfields=None, write_access=True, attributes=None):
		"""
			extending untuk fields_get 
			the fields_get() method is used by the web client to query for the
			fields of the model and their properties. It returns a Python dictionary mapping field names to
			a dictionary of field attributes, such as the display string or the help string. What interests
			us is the readonly attribute, which we force to True if the user is not a library manager. This
			will make the field read only in the web client, which will avoid unauthorized users from trying
			to edit it only to be faced with an error message.
		"""
		fields = super(LibraryBook, self).fields_get(allfields=allfields, write_access=write_access, attributes=attributes)
		
		if not self.user_has_groups('library.group_library_manager'):
			if 'manager_remarks' in fields:
				fields['manager_remarks']['readonly'] = True

