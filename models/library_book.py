# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.addons import decimal_precision as dp
from openerp.fields import Date as fDate
from datetime import timedelta as td


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = 'name'
    book_ids = fields.One2many(
        'library.book', 'publisher_id',
        string='Published Books'
        )
    book_ids = fields.Many2many(
        'library.book',
        string='Authored Books',
        # relation='library_book_res_partner_rel'  # optional
        )
    authored_book_ids = fields.Many2many(
        'library.book', string='Authored Books'
        )
    count_books = fields.Integer(
        'Number of Authored Books',
        compute='_compute_count_books'
        )


    # add the method needed to compute the book count
    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)



# Add the abstract model for the archive feature.
# It must be defined in the Library Book model, where it will be used
class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    active = fields.Boolean(default=True)

    def do_action(self):
        for record in self:
            record.active = not record.active



class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = 'base.archive' #
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
         ('borrowed', 'Borrowec'),
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
    publisher_city = fields.Char(
        'Publisher City', related='publisher_id.city'
        )
    author_ids = fields.Many2many('res.partner', string='Authors')
    age_days = fields.Float(
        string='Days Since Release',
        compute='_compute_age',
        inverse='_inverse_age',
        search='_search_age',
        store=False,
        compute_sudo=False,
        )
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()

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

    #add the method with the value computation logic
    @api.depends('date_release')
    def _compute_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            delta = (fDate.from_string(book.date_release - today))
            book.age_days = delta.days

    #add the method implementing the logic to write on the computed field
    def _inverse_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            d = td(days=book.age_days) - today
            book.date_release = fDate.to_string(d)

    #To implement the logic allowing you to search on the computed field
    def _search_age(self, operator, value):
        today = fDate.from_string(fDate.today())
        value_days = td(days=value)
        value_date = fDate.to_string(today - value_days)
        return [('date_release', operator, value_date)]


    #add a helper method to dynamically build the list of selectable target models
    @api.model
    def _referencable_models(self):
        models = self.env['res.request.link'].search([])
        return [(x.object, x.name) for x in models]

    #add the Reference field and use the previous function to provide the list of selectable models
    ref_doc_id = fields.Reference(
        selection='_referencable_models',
        string='Reference Document'
        )

    # Add a helper method to check whether a state transition is allowed:
    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('available', 'lost'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]
        return (old_state, new_state) in allowed

    # Add a method to change the state of some books to a new one passed as an argument:
    @api.multi
    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                continue


    @api.model
    def get_all_library_members(self):
        library_member_model = self.env['library.member']
        return library_member_model.search([])



# 1. Add the new model, inheriting from res.partner :
class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}
    partner_id = fields.Many2one(
        'res.partner',
        ondelete='cascade'
        )






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
