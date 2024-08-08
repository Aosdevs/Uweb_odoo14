# Copyright (C) 2021 - WATTIO dev@wattio.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from dateutil.relativedelta import relativedelta

from odoo import fields, models


class MailingTrace(models.Model):

    _inherit = 'mailing.trace'

    def get_scheduled(self, mailing_id):
        """ VERIFICAR SE PROCEDE """
        start_date = fields.Datetime.now() + relativedelta(hours=-3)

        if mailing_id.trigger_type_time == "minutes":
            start_date += relativedelta(minutes=mailing_id.trigger_qty_time)

        if mailing_id.trigger_type_time == "hours":
            start_date += relativedelta(hours=mailing_id.trigger_qty_time)

        if mailing_id.trigger_type_time == "days":
            start_date += relativedelta(days=mailing_id.trigger_qty_time)

        return start_date

    def get_mailing(self, trigger):
        """ Get mailing  off campaign from mailing.trace """
        mailing_id = self.env["mailing.mailing"].search([
            ("campaign_id", "=", self.campaign_id.id),
            ("trigger", "=", trigger),
            ("trigger_mailing_id", "=", self.mass_mailing_id.id),
            ("mailing_type", "=", self.trace_type),
        ], limit=1)

        return mailing_id

    def set_opened(self, mail_mail_ids=None, mail_message_ids=None):
        """   """
        traces = super(MailingTrace, self).\
                set_opened(mail_mail_ids, mail_message_ids)

        mailing_id = traces.get_mailing("message_opened")
        if mailing_id:
            scheduled = self.get_scheduled(mailing_id)
            mailing_id.action_send_mail([traces.res_id], scheduled_date=scheduled)

        return traces

    def set_clicked(self, mail_mail_ids=None, mail_message_ids=None):
        """   """
        traces = super(MailingTrace, self).\
            set_clicked(mail_mail_ids, mail_message_ids)

        mailing_id = traces.get_mailing("message_clicked")
        if mailing_id:
            scheduled = self.get_scheduled(mailing_id)
            mailing_id.action_send_mail([traces.res_id], scheduled_date=scheduled)

        return traces

    def set_replied(self, mail_mail_ids=None, mail_message_ids=None):
        """   """
        traces = super(MailingTrace, self).\
            set_replied(mail_mail_ids, mail_message_ids)

        mailing_id = traces.get_mailing("message_replied")
        if mailing_id:
            scheduled = self.get_scheduled(mailing_id)
            mailing_id.action_send_mail([traces.res_id], scheduled_date=scheduled)

        return traces

    def set_bounced(self, mail_mail_ids=None, mail_message_ids=None):
        """   """
        traces = super(MailingTrace, self).\
            set_bounced(mail_mail_ids, mail_message_ids)

        mailing_id = traces.get_mailing("message_bounced")
        if mailing_id:
            scheduled = self.get_scheduled(mailing_id)
            mailing_id.action_send_mail([traces.res_id], scheduled_date=scheduled)

        return traces
