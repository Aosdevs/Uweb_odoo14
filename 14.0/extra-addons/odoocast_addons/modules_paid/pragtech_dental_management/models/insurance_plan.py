from odoo import fields, models, api

class InsurancePlan(models.Model):
    _name = 'medical.insurance.plan'
    _description = "Medical Insurance Plan"

    # @api.depends('name', 'code')
    # def name_get(self):
    #     result = []
    #     for insurance in self:
    #         name = insurance.code + ' ' + insurance.name.name
    #         result.append((insurance.id, name))
    #     return result

    is_default = fields.Boolean(
        string='Default Plan', 
        help='Check if this is the default plan when assigning this insurance company to a patient')
    
    name = fields.Char(
        related='product_insurance_plan_id.name')
    
    product_insurance_plan_id = fields.Many2one(
        'product.product',
        string='Plan',
        required=True,
        domain="[('type', '=', 'service'), ('is_insurance_plan', '=', True)]",
        help='Insurance company plan')
    
    company_id = fields.Many2one(
        'res.partner', 
        string='Insurance Company', 
        required=True, 
        domain="[('is_insurance_company', '=', '1')]")
    
    notes = fields.Text('Extra info')
    
    code = fields.Char(size=64, required=True, index=True)