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
    huespedes_ids = fields.Many2many('res.partner', string=_('Huespedes'), required=True)
    
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
        result = super(Entrada, self).create(vals_list)
        for rec in result:
            rec.habitacion_id.estado = 'ocupada'
            rec.reserva_id.active = False
        return result
    
    @api.constrains('huespedes_ids')
    def _constrains_huespedes_ids(self):
        for rec in self:
            if len(rec.huespedes_ids) > rec.habitacion_id.capacidad:
                raise ValidationError(f'La capacidad de esta habitación es de {rec.habitacion_id.capacidad} huéspedes')
            elif len(rec.huespedes_ids) < 1:
                raise ValidationError('Debe haber al menos 1 huésped')
    