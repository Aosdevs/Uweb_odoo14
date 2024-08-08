# Copyright (C) 2021 - WATTIO dev@wattio.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from datetime import datetime

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class Crmstage(models.Model):
    _inherit = 'crm.stage'

    crm_lead_ids = fields.One2many(
        comodel_name="crm.lead",
        inverse_name="stage_id"
    )