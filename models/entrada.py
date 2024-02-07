# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Entrada(models.Model):
    _name = 'hotel.entrada'
    _inherit = ['mail.thread']
    _description = _('Entrada al hotel')

    name = fields.Char(string=_('Nº'), default=lambda self: _('Registrar Entrada'), readonly=True)
    reserva_id = fields.Many2one('hotel.reservacion', string=_('Reservación'), readonly=True)
    habitacion_id = fields.Many2one('hotel.habitacion', string=_('Habitación'), readonly=True)
    huespedes_ids = fields.Many2many('res.partner', string=_('Huespedes'))
    
    def registrar_estancia(self):
        return{
            'res_model': 'hotel.estancia',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('hotel.view_hotel_estancia_form').id
        }
    
    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('name', _('Registrar Entrada')) == _('Registrar Entrada'):
                val['name'] = self.env['ir.sequence'].next_by_code('hotel.entrada') or _('Registrar Entrada')
        return super(Entrada, self).create(vals_list)