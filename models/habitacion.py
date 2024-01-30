# -*- coding: utf-8 -*-
from email.policy import default
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.populate import compute

_logger = logging.getLogger(__name__)


class Habitacion(models.Model):
    _name = 'hotel.habitacion'
    _description = _('Habitación del hotel')

    name = fields.Char(string=_('Nº'), default="Nueva Habitación", compute='_compute_name')
    numero = fields.Integer(string=_('Número'), default="1", required=True)
    tipo = fields.Selection(
        string=_('Tipo de habitación'),
        required=True,
        selection=[
            ('simple', 'Simple'),
            ('doble', 'Doble'),
            ('suite', 'Suite'),
            ('jrsuite', 'Junior Suite'),
        ]
    )
    capacidad = fields.Integer(string=_('Capacidad'), compute='_compute_capacidad', default="0")
    currency_id = fields.Many2one('res.currency', 'Moneda', required=True, default=lambda self: self.env['res.currency'].search([('name', '=', 'CUP')]).id)
    precio_por_noche = fields.Monetary(string=_('Precio por noche'), required=True)

    
    @api.depends('numero')
    def _compute_name(self):
        for rec in self:
            rec.name = f'Habitación {rec.numero}'
            
    @api.depends('tipo')
    def _compute_capacidad(self):
        for rec in self:
            if rec.tipo == 'simple':
                rec.capacidad = 1
            elif rec.tipo == 'doble':
                rec.capacidad = 2
            elif rec.tipo == 'jrsuite':
                rec.capacidad = 3
            elif rec.tipo == 'suite':
                rec.capacidad = 4
            else:
                rec.capacidad = 0
    
    @api.constrains('precio_por_noche')
    def _check_precios(self):
        for rec in self:
            if rec.precio_por_noche <= 0:
                raise ValidationError('El precio por noche debe ser mayor que 0')
        
    