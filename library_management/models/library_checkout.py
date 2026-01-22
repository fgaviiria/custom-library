# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LibraryCheckout(models.Model):
    """ This model represents library.checkout."""
    _name = 'library.checkout'
    _description = 'LibraryCheckout'

    book_id = fields.Many2one('library.book', string='Book', required=True, domain=[('is_available', '=', True)])
    member_id = fields.Many2one('library.member', string='Member', required=True)
    checkout_date = fields.Date(string='Checkout Date', default=fields.Date.context_today, required=True)
    return_date = fields.Date(string='Return Date')
    state = fields.Selection([
        ('on_loan', 'On Loan'),
        ('returned', 'Returned'),
    ], string='State', default='on_loan', required=True)

    @api.constrains('book_id')
    def _check_book_availability(self):
        for record in self:
            if record.state == 'on_loan' and not record.book_id.is_available:
                raise ValidationError('The book "%s" is not available.' % record.book_id.name)

    @api.model_create_multi
    def create(self, vals_list):
        checkouts = super(LibraryCheckout, self).create(vals_list)
        for checkout in checkouts:
            if checkout.state == 'on_loan':
                checkout.book_id.is_available = False
        return checkouts

    def write(self, vals):
        if 'book_id' in vals:
            for record in self:
                if record.state == 'on_loan':
                    record.book_id.is_available = True

        result = super(LibraryCheckout, self).write(vals)

        if 'state' in vals or 'book_id' in vals:
            for record in self:
                if record.state == 'returned':
                    record.book_id.is_available = True
                elif record.state == 'on_loan':
                    record.book_id.is_available = False
        return result

    def action_return_book(self):
        """Action button to return the book"""
        for record in self:
            if record.state == 'on_loan':
                record.write({
                    'state': 'returned',
                    'return_date': fields.Date.today() if not record.return_date else record.return_date
                })
