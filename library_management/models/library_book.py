# -*- coding: utf-8 -*-
from odoo import api, fields, models
import requests
from dateutil import parser

class LibraryBook(models.Model):
    """ This model represents library.book."""
    _name = 'library.book'
    _description = 'LibraryBook'

    name = fields.Char(string='Title')
    author = fields.Char(string='Author')
    publication_date = fields.Date(string='Published Date')
    isbn = fields.Char(string='ISBN', required=True)
    is_available = fields.Boolean(string='Is Available', default=True)
    checkout_ids = fields.One2many('library.checkout', 'book_id', string='Checkouts')

    _sql_constraints = [
        ('isbn_unique', 'UNIQUE(isbn)', 'The ISBN must be unique!')
    ]

    def search_book_by_isbn(self, isbn):
        """Search for a book data from Open Library API using ISBN."""
        isbn_clean = isbn.replace('-', '').replace(' ', '')

        url = 'https://openlibrary.org/api/books'
        params = {
            'bibkeys': f'ISBN:{isbn_clean}',
            'format': 'json',
            'jscmd': 'data'
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            book_data = data.get(f'ISBN:{isbn_clean}', {})
            if not book_data:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Not Found',
                        'message': f'No data found for ISBN: {isbn}',
                        'type': 'warning',
                    }
                }
            raw_date = book_data.get('publish_date')
            if raw_date:
                try:
                    book_data['publish_date'] = parser.parse(raw_date).date()
                except (ValueError, TypeError):
                    book_data['publish_date'] = None
            return {
                'name': book_data.get('title', ''),
                'author': ', '.join(author['name'] for author in book_data.get('authors', [])),
                'publication_date': book_data.get('publish_date'),
                'isbn': isbn
            }
        except requests.RequestException:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': 'Failed to fetch book data from Open Library API.',
                    'type': 'danger',
                }
            }

    def action_fetch_book_data(self):
        """Action button to fetch book data by ISBN."""
        for record in self:
            if record.isbn:
                book_data = self.search_book_by_isbn(record.isbn)
                if isinstance(book_data, dict) and not book_data.get('type'):
                    record.write({
                        'name': book_data.get('name', record.name),
                        'author': book_data.get('author', record.author),
                        'publication_date': book_data.get('publication_date') or record.publication_date
                    })

                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'title': 'Success',
                            'message': 'Book data fetched successfully.',
                            'type': 'success',
                        }
                    }
                else:
                    return book_data

    @api.onchange('isbn')
    def _onchange_isbn(self):
        """Onchange to fetch book data when ISBN is changed."""
        for record in self:
            if record.isbn:
                book_data = self.search_book_by_isbn(record.isbn)
                if isinstance(book_data, dict) and not book_data.get('type'):
                    record.name = book_data.get('name', record.name)
                    record.author = book_data.get('author', record.author)
                    record.publication_date = book_data.get('publication_date') or record.publication_date
