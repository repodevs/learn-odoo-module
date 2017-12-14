# -*- coding: utf-8 -*-
from openerp import models, fields


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'

    name = fields.Char('Title', required=True)
    author_ids = fields.Many2many('res.partner', string='Authors')
    short_name = fields.Char(
        string='Short Title',
        size=100, # For Char Only
        translate=False, # also for Text fields
        )
    notes = fields.Text('Internal Notes')
    state = fields.Selection(
        [('draft', 'Not Available'),
         ('available', 'Available'),
         ('lost', 'Lost')],
        'State')
    description = fields.Html(
        string='Description',
        # Optional:
        sanitize=True,
        strip_style=False,
        translate=False,
        )
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date')
    date_updated = fields.Date('Last Updated')
    pages = fields.Integer(
        string='Number of Pages',
        default=0,
        help='Total book page count',
        groups='base.group_user',
        states={'cancel':[('readonly', True)]},
        copy=True,
        index=False,
        readonly=False,
        required=False,
        company_dependent=False,
        )
    render_rating = fields.Float(
        'Reader Avarage Rating',
        (14, 4) # Optional precision (total, decimals),
        )
