# -*- coding: utf-8 -*-
import base64
import logging

from odoo import models, fields, api, _, modules
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

def _get_default_image():
        image_path = modules.get_module_resource('hotel', 'static/src/img', 'habitacion.png')
        return base64.b64encode(open(image_path, 'rb').read())

class Habitacion(models.Model):
    _name = 'hotel.habitacion'
    _description = _('Habitación del hotel')
    _order = 'name'

    name = fields.Char(string=_('Nº'), default="Nueva Habitación")
    numero = fields.Integer(string=_('Número'), required=True)
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
    image = fields.Binary(string=_('Imagen'), default=_get_default_image())
    estado = fields.Selection(
        string=_('Estado'),
        selection=[
            ('disponible', 'Disponible'),
            ('ocupada', 'Ocupada'),
        ],
        default="disponible"
    )

    _sql_constraints = [('numero_unico', 'unique (numero)', 'Ya existe una habitación con este número')]
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = f"Habitación {vals['numero']}"
        return super(Habitacion, self).create(vals_list)
    
    # @api.depends('numero')
    # def _compute_name(self):
    #     for rec in self:
    #         rec.name = f'Habitación {rec.numero}'
            
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
        
    