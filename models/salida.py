# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Salida(models.Model):
    _name = 'hotel.salida'
    _description = _('Salida')

    name = fields.Char(_('Name'))
