# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Estancia(models.Model):
    _name = 'hotel.estancia'
    _inherit = ['mail.thread']
    _description = _('Estancia en el hotel')

    name = fields.Char(string=_('Nº'), default=lambda self: _('Registrar Estancia'), readonly=True)
    reserva_id = fields.Many2one('hotel.reservacion', string=_('Reservación'), readonly=True)
    habitacion_id = fields.Many2one('hotel.habitacion', string=_('Habitación'), readonly=True)
    entrada_id = fields.Many2one('hotel.entrada')
    huespedes_ids = fields.Many2many('res.partner', string=_('Huespedes'), readonly=True, store=True)
    fecha_entrada = fields.Date(string=_('Fecha de entrada'), readonly=True, compute="_compute_fechas", store=True)
    fecha_salida = fields.Date(string=_('Fecha de salida'), readonly=True, compute="_compute_fechas", store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('name', _('Registrar Estancia')) == _('Registrar Estancia'):
                val['name'] = self.env['ir.sequence'].next_by_code('hotel.estancia') or _('Registrar Estancia')
        result = super(Estancia, self).create(vals_list)
        for rec in result:
            rec.entrada_id.tiene_estancia = True
        return result
    
    @api.depends('reserva_id')
    def _compute_fechas(self):
        for rec in self:
            rec.fecha_entrada = rec.reserva_id.fecha_entrada
            rec.fecha_salida = rec.reserva_id.fecha_salida