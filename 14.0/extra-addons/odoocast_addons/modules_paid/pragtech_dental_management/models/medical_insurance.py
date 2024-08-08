from odoo import fields, models, api

class MedicalInsurance(models.Model):
    _name = "medical.insurance"
    _description = "Medical Insurance"
    _rec_name = "name"

    @api.depends('number', 'company_id')
    def name_get(self):
        result = []
        for insurance in self:
            name = insurance.company_id.name + ':' + insurance.number
            result.append((insurance.id, name))
        return result

    name = fields.Char(related="res_partner_insurance_id.name")
    res_partner_insurance_id = fields.Many2one('res.partner', 'Owner')
    number = fields.Char('Number', size=64, required=True)
    company_id = fields.Many2one('res.partner', 'Insurance Company',
                                 domain="[('is_insurance_company', '=', '1')]",
                                 required=True)
    member_since = fields.Date('Member since')
    member_exp = fields.Date('Expiration date')
    category = fields.Char('Category', size=64,
                           help="Insurance company plan / category")
    type = fields.Selection(
        [('state', 'State'), ('labour_union', 'Labour Union / Syndical'),
         ('private', 'Private'), ],
        'Insurance Type')
    notes = fields.Text('Extra Info')
    plan_id = fields.Many2one('medical.insurance.plan', 'Plan',
                              help='Insurance company plan')
