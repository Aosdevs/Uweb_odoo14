# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MedicalPatient(models.Model):
    _inherit = 'medical.patient'

    referring_doctor_idd = fields.Many2one('medical.physician',
                                           'Referring  Doctor', required=False)

class ReferringDoctor(models.TransientModel):
    _name = 'referring.doctor.wizard'
    _description = 'referring doctor wizard'





    name = fields.Char(related='referring_doctor_id.name')
    date_from = fields.Datetime(string="Date From", required=True, )
    date_to = fields.Datetime(string="Date To", required=True, )
    referring_doctor_id = fields.Many2one('medical.physician',
                                          'Referring  Doctor', required=True)
    self_commission = fields.Float(string="Self Commission %",  required=False,default=20 )
    other_commission = fields.Float(string="Other Commission %",  required=False,default=10 )





    def export_referring_doctor(self):
        for rec in self:
            return self.env.ref('report_referral_doctor.report_action_id_referring_doctor').report_action(self)

