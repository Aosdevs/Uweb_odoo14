# Copyright (C) 2020 - SUNNIT dev@sunnit.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from dateutil.relativedelta import relativedelta


def define_time_trigger(mailing_id, start_date):
    if mailing_id.trigger_type_time == "minutes":
        start_date += relativedelta(minutes=mailing_id.trigger_qty_time)

    if mailing_id.trigger_type_time == "hours":
        start_date += relativedelta(hours=mailing_id.trigger_qty_time)

    if mailing_id.trigger_type_time == "days":
        start_date += relativedelta(days=mailing_id.trigger_qty_time)

    return start_date