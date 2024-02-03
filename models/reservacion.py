# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Reservacion(models.Model):
    _name = 'hotel.reservacion'
    _inherit = ['mail.thread']
    _description = _('Reservación')
    _order = 'name'

    name = fields.Char(_('Name'))
