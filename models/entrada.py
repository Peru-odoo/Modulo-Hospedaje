# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Entrada(models.Model):
    _name = 'hotel.entrada'
    _inherit = ['mail.thread']
    _description = _('Entrada')

    name = fields.Char(string=_('Nº'), default=lambda self: _('Registrar Entrada'), readonly=True)
    reserva_id = fields.Many2one('hotel.reservacion', string=_('Reservación'), readonly=True)
    habitacion_id = fields.Many2one('hotel.habitacion', string=_('Habitación'), readonly=True)
    huespedes_ids = fields.Many2many('res.partner', string=_('Huespedes'))