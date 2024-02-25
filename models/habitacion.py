# -*- coding: utf-8 -*-
import base64
import logging

from odoo import models, fields, api, _, modules
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

def _get_default_image():
        image_path = modules.get_module_resource('hospedaje', 'static/src/img', 'habitacion.png')
        return base64.b64encode(open(image_path, 'rb').read())

class Habitacion(models.Model):
    _name = 'hospedaje.habitacion'
    _inherit = ['mail.thread']
    _description = _('Habitación')
    _order = 'numero'

    name = fields.Char(string=_('Nº'), compute="_compute_name", default="Nueva Habitación", tracking=True)
    numero = fields.Integer(string=_('Número'), required=True, tracking=True)
    tipo = fields.Many2one('hospedaje.habitacion.tipo', string=_('Tipo de habitación'), required=True, tracking=True)
    capacidad = fields.Integer(string=_('Capacidad'), compute='_compute_capacidad', default="0")
    currency_id = fields.Many2one('res.currency', 'Moneda', required=True, default=lambda self: self.env.company.currency_id)
    precio_por_noche = fields.Monetary(string=_('Precio por noche'), required=True, tracking=True)
    image = fields.Binary(string=_('Imagen'), default=_get_default_image(), tracking=True)
    estado = fields.Selection(
        string=_('Estado'),
        selection=[
            ('disponible', 'Disponible'),
            ('ocupada', 'Ocupada'),
        ],
        default="disponible", tracking=True, readonly=True
    )

    _sql_constraints = [('numero_unico', 'unique (numero)', 'Ya existe una habitación con este número')]
     
    def name_get(self):
        res = []
        for rec in self:
            name = f'{rec.name} - {rec.tipo.name} - {rec.precio_por_noche}{rec.currency_id.symbol}'
            res.append((rec.id, name))
        return res
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('numero', operator, name), ('tipo', operator, name)]
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)
            
    @api.depends('numero')
    def _compute_name(self):
        for rec in self:
            rec.name = f"Habitación {rec.numero}"
        
    @api.depends('tipo')
    def _compute_capacidad(self):
        for rec in self:
            rec.capacidad = rec.tipo.capacidad
    
    @api.constrains('precio_por_noche')
    def _check_precios(self):
        for rec in self:
            if rec.precio_por_noche <= 0:
                raise ValidationError('El precio por noche debe ser mayor que 0')
            
    @api.constrains('numero')
    def _check_numero(self):
        for rec in self:
            if rec.numero < 1:
                raise ValidationError('El número de la habitación debe ser mayor que 0')
           
     
    
    