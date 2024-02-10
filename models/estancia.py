# -*- coding: utf-8 -*-
import logging
import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, AccessDenied

_logger = logging.getLogger(__name__)


class Estancia(models.Model):
    _name = 'hotel.estancia'
    _inherit = ['mail.thread']
    _description = _('Estancia en el hotel')

    name = fields.Char(string=_('Nº'), default=lambda self: _('Registrar Estancia'), readonly=True)
    active = fields.Boolean(default=True, tracking=True)
    reserva_id = fields.Many2one('hotel.reservacion', string=_('Reservación'), readonly=True)
    habitacion_id = fields.Many2one('hotel.habitacion', string=_('Habitación'), readonly=True)
    entrada_id = fields.Many2one('hotel.entrada')
    huespedes_ids = fields.Many2many('res.partner', string=_('Huespedes'), readonly=True, store=True)
    fecha_entrada = fields.Date(string=_('Fecha de entrada'), readonly=True, compute="_compute_fechas", store=True)
    fecha_salida = fields.Date(string=_('Fecha de salida'), readonly=True, compute="_compute_fechas", store=True)
    pedidos_ids = fields.Many2many('hotel.pedido', string=_('Pedidos'))
    tiene_salida = fields.Boolean(default=False)

    def agregar_pedido(self):
        return{
            'res_model': 'hotel.pedido',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('hotel.view_hotel_pedido_form').id
        }
        
    def registrar_salida(self):
        for rec in self:
            fecha = datetime.datetime.now() + datetime.timedelta(hours=-5)
            fecha_hoy = datetime.date(fecha.year, fecha.month, fecha.day)
            if rec.fecha_salida != fecha_hoy:
                raise AccessDenied('No estamos en la fecha de salida planificada')
        return{
            'res_model': 'hotel.salida',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('hotel.view_hotel_salida_form').id
        }

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