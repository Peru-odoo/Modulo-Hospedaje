# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Salida(models.Model):
    _name = 'hotel.salida'
    _description = _('Salida')

    name = fields.Char(string=_('Nº'), default=lambda self: _('Registrar Salida'), readonly=True)
    estancia_id = fields.Many2one('hotel.estancia', string=_('Estancia'), readonly=True)
    habitacion_id = fields.Many2one('hotel.habitacion', string=_('Habitación'), readonly=True)
    huespedes_ids = fields.Many2many('res.partner', string=_('Huéspedes'), readonly=True)
    
    
    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('name', _('Registrar Salida')) == _('Registrar Salida'):
                val['name'] = self.env['ir.sequence'].next_by_code('hotel.salida') or _('Registrar Salida')
        result = super(Salida, self).create(vals_list)
        for rec in result:
            rec.estancia_id.tiene_salida = True
            rec.estancia_id.active = False
            rec.habitacion_id.estado = 'disponible'
        return result
