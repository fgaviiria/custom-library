# -*- coding: utf-8 -*-
import logging
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo import fields

_logger = logging.getLogger(__name__)


class TestLibraryManagement(TransactionCase):

    def setUp(self):
        super(TestLibraryManagement, self).setUp()
        _logger.info('--- SET UP: Creando datos de prueba ---')
        self.book = self.env['library.book'].create({
            'name': 'Odoo Development Cookbook',
            'isbn': '978-1785281',
            'is_available': True
        })
        self.member = self.env['library.member'].create({
            'name': 'Test Member',
            'member_id': 'MEM001'
        })

    def test_01_checkout_flow(self):
        """Test standard checkout and return flow"""
        _logger.info('--- TEST 01: Iniciando flujo de préstamo ---')

        # 1. Crear préstamo
        checkout = self.env['library.checkout'].create({
            'book_id': self.book.id,
            'member_id': self.member.id,
        })
        _logger.info('Préstamo creado. Estado del libro: %s', self.book.is_available)

        self.assertFalse(self.book.is_available, "Book should be unavailable after checkout")

        # 2. Devolver libro
        _logger.info('Devolviendo el libro...')
        checkout.action_return_book()

        self.assertTrue(self.book.is_available, "Book should be available after return")
        _logger.info('--- TEST 01: Éxito ---')

    def test_02_constraint_unavailable_book(self):
        """Test constraint: Cannot checkout unavailable book"""
        _logger.info('--- TEST 02: Probando constraint de disponibilidad ---')

        # Primer préstamo
        self.env['library.checkout'].create({
            'book_id': self.book.id,
            'member_id': self.member.id,
        })

        # Intentar prestar el MISMO libro
        _logger.info('Intentando prestar un libro ya ocupado (se espera error)...')
        with self.assertRaises(ValidationError):
            self.env['library.checkout'].create({
                'book_id': self.book.id,
                'member_id': self.member.id,
            })
        _logger.info('--- TEST 02: Constraint funcionó correctamente ---')
