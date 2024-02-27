# -*- coding: utf-8 -*-
import datetime
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, AccessDenied

_logger = logging.getLogger(__name__)


class Reservacion(models.Model):
    _name = 'hospedaje.reservacion'
    _inherit = ['mail.thread']
    _description = _('Reservación')
    _order = 'fecha_entrada'

    name = fields.Char(string=_('Nº'), default=lambda self: _('Nueva Reservación'), readonly=True)
    active = fields.Boolean(default=True)
    fecha_entrada = fields.Date(
        string=_('Fecha de entrada'),
        default=fields.Date.context_today,
        required=True,
    )
    cantidad_dias = fields.Integer(string=_('Cantidad de días'), required=True, default=1)
    fecha_salida = fields.Date(
        string=_('Fecha de salida'),
        compute='_compute_fecha_salida',
        store=True
    )
    estado = fields.Selection(
        string=_('Estado'),
        selection=[
            ('pendiente', 'Pendiente'),
            ('encurso', 'En Curso'),
            ('finalizada', 'Finalizada'),
            ('cancelada', 'Cancelada')
        ],
        default='pendiente', tracking=True, readonly=True
    )
    entrada_id = fields.Many2one('hospedaje.entrada', string='Entrada', readonly=True)
    huespedes_ids = fields.Many2many('res.partner', compute='_compute_huespedes_ids', string='huespedes_ids')
    
    @api.depends('entrada_id')
    def _compute_huespedes_ids(self):
        for rec in self:
            rec.huespedes_ids = rec.entrada_id.huespedes_ids
    
    def _get_cliente_domain(self):
        domain = [('id', 'in', 
                   self.env['res.partner'].search([('huesped', '=', True)]).ids)]
        return domain
    cliente_id = fields.Many2one('res.partner', string=_('Cliente'), required=True, domain=_get_cliente_domain)
    
    habitacion_id = fields.Many2one('hospedaje.habitacion', string=_('Habitación'), required=True)
    
    def registrar_entrada(self):
        for rec in self:
            fecha = datetime.datetime.now() + datetime.timedelta(hours=-5)
            fecha_hoy = datetime.date(fecha.year, fecha.month, fecha.day)
            if rec.fecha_entrada != fecha_hoy:
                raise AccessDenied('No estamos en la fecha de entrada reservada')
        return{
            'res_model': 'hospedaje.entrada',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('hospedaje.view_hospedaje_entrada_form').id
        }
        
    def registrar_salida(self):
        for rec in self:
            fecha = datetime.datetime.now() + datetime.timedelta(hours=-5)
            fecha_hoy = datetime.date(fecha.year, fecha.month, fecha.day)
            if rec.fecha_salida > fecha_hoy:
                raise AccessDenied('No estamos en la fecha de salida planificada')
        self.env['hospedaje.salida'].create({
            'reserva_id': self.id,
            'habitacion_id': self.habitacion_id.id,
            'huespedes_ids': self.huespedes_ids.ids
        })
        
    def cancelar_reservacion(self):
        for rec in self:
            rec.estado = 'cancelada'
            rec.active = False
    
    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('name', _('Nueva Reservación')) == _('Nueva Reservación'):
                val['name'] = self.env['ir.sequence'].next_by_code('hospedaje.reservacion') or _('Nueva Reservación')
        result = super(Reservacion, self).create(vals_list)
        for rec in result:
            rec.cliente_id.huesped = True
        return result
    
    @api.depends('fecha_entrada', 'cantidad_dias')
    def _compute_fecha_salida(self):
        for rec in self:
            if rec.fecha_entrada and rec.cantidad_dias and rec.cantidad_dias > 0:
                rec.fecha_salida = rec.fecha_entrada + datetime.timedelta(days=rec.cantidad_dias)
            else:
                rec.fecha_salida = ''
                
    @api.onchange('fecha_salida')
    def _dominio_habitaciones(self):
        habitaciones = self.env['hospedaje.habitacion'].search([]).ids
        reservaciones = self.env['hospedaje.reservacion'].search(['|', ('estado', '=', 'pendiente'), ('estado', '=', 'encurso')])
        for reservacion in reservaciones:
            if reservacion.fecha_entrada < self.fecha_salida and reservacion.fecha_salida > self.fecha_entrada:
                habitaciones.remove(reservacion.habitacion_id.id)
        domain = {'habitacion_id': [('id', 'in', habitaciones)]}
        return {'domain': domain}
                
    @api.constrains('cantidad_dias')
    def _constrains_cantidad_dias(self):
        for rec in self:
            if rec.cantidad_dias < 1:
                raise ValidationError('La cantidad de días debe ser mayor que 0')
            
    @api.constrains('fecha_entrada')
    def _constrains_fecha_entrada(self):
        for rec in self:
            fecha = datetime.datetime.now() + datetime.timedelta(hours=-5)
            fecha_hoy = datetime.date(fecha.year, fecha.month, fecha.day)
            if rec.fecha_entrada < fecha_hoy:
                raise ValidationError('La fecha de entrada ya ha pasado')
