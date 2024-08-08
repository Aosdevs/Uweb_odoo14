# Copyright (C) 2020 - SUNNIT dev@sunnit.com.br
# Copyright (C) 2021 - WATTIO dev@wattio.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailTemplate(models.Model):
    _inherit = "mail.template"

    body_arch = fields.Html(string='Body Arch', translate=False)

    mass_mailing_automation = fields.Boolean(
        string="Use template in Mass Mailing Marketing",
    )
