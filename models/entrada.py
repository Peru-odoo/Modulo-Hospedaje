# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Entrada(models.Model):
    _name = 'hotel.entrada'
    _inherit = ['mail.thread']
    _description = _('Entrada')

    name = fields.Char(_('Name'))
