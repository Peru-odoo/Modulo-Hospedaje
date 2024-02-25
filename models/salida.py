# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Salida(models.Model):
    _name = 'hospedaje.salida'
    _description = _('Salida')

    name = fields.Char(string=_('Nº'), default=lambda self: _('Registrar Salida'), readonly=True)
    reserva_id = fields.Many2one('hospedaje.reservacion', string=_('Reservación'), readonly=True)
    habitacion_id = fields.Many2one('hospedaje.habitacion', string=_('Habitación'), readonly=True)
    huespedes_ids = fields.Many2many('res.partner', string=_('Huéspedes'), readonly=True)
    
    
    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('name', _('Registrar Salida')) == _('Registrar Salida'):
                val['name'] = self.env['ir.sequence'].next_by_code('hospedaje.salida') or _('Registrar Salida')
        result = super(Salida, self).create(vals_list)
        for rec in result:
            rec.reserva_id.active = False
            rec.reserva_id.estado = 'atendida'
            rec.habitacion_id.estado = 'disponible'
        return result
