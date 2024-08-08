from . import models
from . import wizard
from . import tools

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
#
#     utm_campaign_1 = env.ref('mass_mailing.mass_mail_campaign_1')
#     utm_campaign_2 = env.ref('mass_mailing_sms.utm_campaign_0')
#     utm_demo_1 = env.ref('utm.campaign_stage_1')
#     utm_demo_2 = env.ref('utm.campaign_stage_2')
#     utm_demo_3 = env.ref('utm.campaign_stage_3')
#
#     if utm_campaign_1:
#         utm_campaign_1.unlink()
#     if utm_campaign_2:
#         utm_campaign_2.unlink()
#
#     if utm_demo_1:
#         utm_demo_1.unlink()
#     if utm_demo_2:
#         utm_demo_2.unlink()
#     if utm_demo_3:
#         utm_demo_3.unlink()
#
    print('\n POST INIT HOOK \n')
