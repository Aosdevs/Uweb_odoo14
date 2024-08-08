import logging
import requests
import json

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta, date
import hashlib

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res.update({'lead_id': self.opportunity_id.id,
                    })
        return res


class AccountMove(models.Model):
    _inherit = 'account.move'

    lead_id = fields.Many2one(comodel_name="crm.lead", string="", required=False, )


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    is_sent = fields.Boolean(string="", )

    def post_facebook_leads(self):
        res_config = self.env['res.config.settings'].search([], order="id desc", limit=1)
        event_id = res_config.event_id
        event_token = res_config.event_token
        if self.partner_id.email:
            mail_str = self.partner_id.email
            mail = hashlib.sha256(mail_str.encode('utf-8')).hexdigest()
        else:
            mail = ''
        if self.partner_id.phone or self.partner_id.mobile:
            phone_str = self.partner_id.phone or self.partner_id.mobile
            phone = hashlib.sha256(phone_str.encode('utf-8')).hexdigest()
        else:
            phone = ''
        fb_api = "https://graph.facebook.com/v15.0/336056881046615/events"
        current_date = datetime.today() - timedelta(hours=2)
        date_int = int(datetime.timestamp(current_date))
        fn = self.partner_id.name
        r = requests.post(fb_api, params={'access_token': event_token
            , 'data':
                                              json.dumps([
                                                  {"action_source": "website", "event_id": '',
                                                   "event_name": event_id, "event_time": date_int,
                                                   "user_data": {
                                                       "client_user_agent": "odoo",
                                                       "em": mail,
                                                       "fn": hashlib.sha256(fn.encode('utf-8')).hexdigest(),
                                                       "ph":phone,
                                                   }, "custom_data": {
                                                      "currency": self.currency_id.name,
                                                      "value": str(self.amount)
                                                  }}

                                              ])
                                          }).json()
        _logger.info(phone,mail,hashlib.sha256(fn.encode('utf-8')).hexdigest())
        if r.get('error'):
            _logger.info(r)
            raise UserError(r['error']['message'])
        self.is_sent = True
        _logger.info('Fetch of leads has ended')
