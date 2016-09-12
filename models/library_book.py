# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.addons import decimal_precision as dp

class ResPartner(models.Model):
    _inherit = 'res.partner'
    book_ids = fields.One2many(
        'library.book', 'publisher_id',
        string='Published Books'
        )
    book_ids = fields.Many2many(
        'library.book',
        string='Authored Books',
        # relation='library_book_res_partner_rel'  # optional
        )


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book' # membuat deskripsi di database
    _order = 'date_release desc, name' #membuat urutan berdasarkan date_release kemudian name
    _rec_name = 'short_name'

    name = fields.Char('Title', required=True)
    short_name = fields.Char('Short Title')
    date_release = fields.Date('Release Date')
    notes = fields.Text('Internal Notes')
    state = fields.Selection(
        [('draft', 'Not Available'),
         ('available', 'Available'),
         ('lost', 'Lost')],
         'State'
         )
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_updated = fields.Datetime('Last Updated')
    description = fields.Html(
            string='Description',
            sanitize=True,
            strip_style=False,
            translate=False,
            )
    pages = fields.Integer(
        string='Number of Pages',
        default=0,
        help='Total book page count',
        groups='base.group_user',
        states={'cancel': [('readonly', True)]},
        copy=True,
        index=False,
        readonly=False,
        required=False,
        company_dependent=False,
        )
    reader_rating = fields.Float(
        'Reader Average Rating',
        (14, 4), # Optional precision (total, decimals)
        )
    cost_price = fields.Float('Book Cost', dp.get_precision('Book Price'))
    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary(
        'Retail Price',
        # (Optional) currency_field='currency_id',
        )
    publisher_id = fields.Many2one(
        'res.partner', string='Publisher',
        # Optional:
        ondelete='set null',
        context={},
        domain=[],
        )
    author_ids = fields.Many2many('res.partner', string='Authors')

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         'Book title must be uniqe..')
    ] #  database constrains

    # python file constrains
    @api.constrains('date_release')
    def _check_release_date(self):
        for r in self:
            if r.date_release > fields.Date.today():
                raise models.ValidationError('Release date must be in the past.')




    # def name_get(self):
    #     """
    #     untuk mendefinisikan name_get
    #     title pada atas halaman ketika saat form view
    #     """
    #     result = []
    #     for record in self:
    #         result.append(
    #             (record.id,
    #             u"%s (%s)" % (record.name, record.date_release)
    #         ))
    #     return result
