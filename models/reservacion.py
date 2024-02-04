# -*- coding: utf-8 -*-
import datetime
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Reservacion(models.Model):
    _name = 'hotel.reservacion'
    _inherit = ['mail.thread']
    _description = _('Reservación')
    _order = 'name'

    name = fields.Char(string=_('Name'), default=lambda self: _('Nueva Reservación'), readonly=True)
    cliente_id = fields.Many2one('res.partner', string='Cliente', required=True)
    habitacion_id = fields.Many2one('hotel.habitacion', string='Habitación', required=True)
    fecha_entrada = fields.Date(
        string=_('Fecha de entrada'),
        default=fields.Date.context_today,
        required=True,
    )
    cantidad_dias = fields.Integer(string=_('Cantidad de días'), required=True)
    fecha_salida = fields.Date(
        string=_('Fecha de salida'),
        compute='_compute_fecha_salida'
    )
    
    
    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('name', _('Nueva Reservación')) == _('Nueva Reservación'):
                val['name'] = self.env['ir.sequence'].next_by_code('hotel.reservacion') or _('Nueva Reservación')
        return super(Reservacion, self).create(vals_list)
    
    @api.depends('fecha_entrada', 'cantidad_dias')
    def _compute_fecha_salida(self):
        for rec in self:
            if rec.fecha_entrada and rec.cantidad_dias and rec.cantidad_dias > 0:
                rec.fecha_salida = rec.fecha_entrada + datetime.timedelta(days=rec.cantidad_dias)
            else:
                rec.fecha_salida = ''
                
    @api.constrains('cantidad_dias')
    def _constrains_cantidad_dias(self):
        for rec in self:
            if rec.cantidad_dias < 1:
                raise ValidationError('La cantidad de días debe ser mayor que 0')
