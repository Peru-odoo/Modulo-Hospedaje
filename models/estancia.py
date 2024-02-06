# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Estancia(models.Model):
    _name = 'hotel.estancia'
    _inherit = ['mail.thread']
    _description = _('Estancia')

    name = fields.Char(_('Name'))
