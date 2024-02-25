# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class TipoHabitacion(models.Model):
    _name = 'hospedaje.habitacion.tipo'
    _inherit = ['mail.thread']
    _description = _('Tipo de habitación')
    
    name = fields.Char(string=_('Nombre'), required=True)
    capacidad = fields.Integer(string=_('Capacidad'), required=True)
    descripcion = fields.Text(string=_('Descripción'))
    
    @api.constrains('capacidad')
    def _constrains_capacidad(self):
        for rec in self:
            if rec.capacidad < 1:
                raise ValidationError('La capacidad debe ser un número positivo')