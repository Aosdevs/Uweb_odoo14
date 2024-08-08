from odoo import fields, models, api

class ClaimManagement(models.Model):
    _name = 'dental.insurance.claim.management'
    _description = 'Dental Insurance Claim Management'

    claim_date = fields.Date(string='Claim Date')
    name = fields.Many2one('medical.patient', string='Patient')
    insurance_company = fields.Many2one('res.partner',
                                        string='Insurance Company',
                                        domain="[('is_insurance_company', '=', True)]")
    insurance_policy_card = fields.Char(string='Insurance Policy Card')
    treatment_done = fields.Boolean(string='Treatment Done')


#     ,domain="[('is_patient', '=', True)]"