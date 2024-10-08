# Copyright (C) 2020 - SUNNIT dev@sunnit.com.br
# Copyright (C) 2021 - Rafael Lima <rafaelslima.py@gmail.com>
# Copyright (C) 2021 - Hendrix Costa <hendrixcosta@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import fields, models


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    scheduled_date = fields.Char(
        string='Scheduled Send Date',
        help="If set, the queue manager will send the email after the date."
             "If not set, the email will be send as soon as possible.",
    )

    def get_mail_values(self, res_ids):
        """ Override method that inject scheduled_date in mail.mail """
        self.ensure_one()
        if 'custom_layout' in self._context and self._context.get('custom_layout') == 'mail.mail_notification_paynow':
            res = super(MailComposeMessage, self).get_mail_values(res_ids)
        else:
            if isinstance(res_ids, list):
                res = super(MailComposeMessage, self).get_mail_values(res_ids)
            else:
                res = super(MailComposeMessage, self).get_mail_values(res_ids.ids)

        if self.scheduled_date:
            for res_id in res:
                mail_values = res[res_id]
                mail_values.update(scheduled_date=self.scheduled_date)

        return res
