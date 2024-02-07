# -*- coding: utf-8 -*-
import datetime
import logging
import zoneinfo

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, AccessDenied

_logger = logging.getLogger(__name__)


class Reservacion(models.Model):
    _name = 'hotel.reservacion'
    _inherit = ['mail.thread']
    _description = _('Reservación')
    _order = 'fecha_entrada'

    name = fields.Char(string=_('Nº'), default=lambda self: _('Nueva Reservación'), readonly=True)
    active = fields.Boolean(default=True, tracking=True)
    cliente_id = fields.Many2one('res.partner', string=_('Cliente'), required=True)
    fecha_entrada = fields.Date(
        string=_('Fecha de entrada'),
        default=fields.Date.context_today,
        required=True,
    )
    cantidad_dias = fields.Integer(string=_('Cantidad de días'), required=True)
    fecha_salida = fields.Date(
        string=_('Fecha de salida'),
        compute='_compute_fecha_salida',
        store=True
    )
    
    def _get_habitacion_domain(self):
        domain = [('id', 'in', 
                   self.env['hotel.habitacion'].search([('estado', '=', 'disponible')]).ids)]
        return domain
    
    habitacion_id = fields.Many2one('hotel.habitacion', string=_('Habitación'), required=True, domain=_get_habitacion_domain)
    
    def registrar_entrada(self):
        for rec in self:
            fecha = datetime.datetime.now() + datetime.timedelta(hours=-5)
            fecha_hoy = datetime.date(fecha.year, fecha.month, fecha.day)
            if rec.fecha_entrada != fecha_hoy:
                raise AccessDenied('No estamos en la fecha de entrada reservada')
        return{
            'res_model': 'hotel.entrada',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('hotel.view_hotel_entrada_form').id
        }
    
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
