# Copyright (C) 2021 - WATTIO dev@wattio.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class MailingListWizard(models.TransientModel):
    _name = "mailing.list.wizard"
    _description = "mailing.list.wizard"

    mailing_contact_ids = fields.Many2many(
        comodel_name="mailing.contact"
    )

    mailing_list_ids = fields.Many2many(
        comodel_name="mailing.list"
    )

    def button_action_add(self):
        for record in self.mailing_contact_ids:
            for singleList_id in self.mailing_list_ids._ids:
                record.list_ids = [(4, singleList_id)]
