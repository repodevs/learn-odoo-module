# -*- coding: utf-8 -*-
from openerp import models, fields

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book' # membuat deskripsi di database
    _order = 'date_release desc, name' #membuat urutan berdasarkan date_release kemudian name
    _rec_name = 'short_name'

    name = fields.Char('Title', required=True)
    short_name = fields.Char('Short Title')
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many('res.partner', string='Authors')


    def name_get(self):
        """
        untuk mendefinisikan name_get
        title pada atas halaman ketika saat form view
        """
        result = []
        for record in self:
            result.append(
                (record.id,
                u"%s (%s)" % (record.name, record.date_release)
            ))
        return result
