# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Pedido(models.Model):
    _name = 'hotel.pedido'
    _description = _('Pedido')

    name = fields.Char(string=_('Nº'), default=lambda self: _('Nuevo Pedido'), readonly=True)
    estancia_id = fields.Many2one('hotel.estancia', string=_('Estancia'), readonly=True)
    descripcion = fields.Text(string=_('Descripción'), required=True)
    
    
    
    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('name', _('Nuevo Pedido')) == _('Nuevo Pedido'):
                val['name'] = self.env['ir.sequence'].next_by_code('hotel.pedido') or _('Nuevo Pedido')
        result = super(Pedido, self).create(vals_list)
        # for rec in result:
        #     rec.estancia_id.pedidos_ids = [(4, [rec.id])]
        return result
