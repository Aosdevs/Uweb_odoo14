# -*- coding: utf-8 -*-
from datetime import date, timedelta
from odoo import models, fields, api

class medical_patient(models.Model):
    _inherit = 'medical.appointment'
    first_appointment = fields.Boolean(string="first appointment",  )

class medical_patient(models.Model):
    _inherit = 'medical.patient'

    first_appointment_date = fields.Datetime(string="First appointment", required=False,compute="get_first_appointment_date" ,store=True)

    @api.depends('patient_id')
    def get_first_appointment_date(self):
        for rec in self:
            appointment=self.env['medical.appointment'].sudo().search([('patient','=',rec.id),('state','=','done')],order='appointment_sdate',limit=1)
            if appointment:
                appointment.first_appointment=True
                rec.first_appointment_date=appointment.appointment_sdate
            else:
                rec.first_appointment_date=False
