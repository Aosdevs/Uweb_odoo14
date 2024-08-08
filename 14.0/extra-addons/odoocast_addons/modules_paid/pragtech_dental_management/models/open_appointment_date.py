from odoo import fields, models, api

class open_appointment_date(models.Model):
    _name = 'open.appointment.date'
    _description = 'New Description'

    date = fields.Date(string="", required=False, )

    def open(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Select lines to purge"),
            "views": [(False, "gantt")],
            "res_model": "medical.appointment",
            'context': {
                'initialDate': self.date}
        }