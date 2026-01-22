# -*- coding: utf-8 -*-
from odoo import fields, models


class LibraryMember(models.Model):
    """ This model represents library.member."""
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = 'LibraryMember'

    partner_id = fields.Many2one('res.partner', string='Partner', required=True, ondelete='cascade')
    member_id = fields.Char(string='Member ID', required=True)
    checkout_ids = fields.One2many('library.checkout', 'member_id', string='Checkouts')
    checkout_count = fields.Integer(string='Number on Loan', compute='_compute_checkout_count')

    _sql_constraints = [
        ('member_id_unique', 'UNIQUE(member_id)', 'The Member ID must be unique!')
    ]

    def _compute_checkout_count(self):
        for record in self:
            record.checkout_count = self.env['library.checkout'].search_count([
                ('member_id', '=', record.id)
            ])

    def action_view_checkouts(self):
        """Action button to view member's checkouts"""
        self.ensure_one()
        return {
            'name': 'Checkouts',
            'type': 'ir.actions.act_window',
            'res_model': 'library.checkout',
            'view_mode': 'list,form',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id},
        }
