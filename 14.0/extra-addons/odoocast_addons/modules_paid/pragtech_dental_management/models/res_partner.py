from odoo import fields, models, api

class Partner(models.Model):
    _inherit = "res.partner"
    _description = "Res Partner"

    def test_merge(self):
        partners = self.sudo().search([("name", "!=", False), ("middle_name", "!=", False)])
        for rec in partners:
            # name =rec.name+" "+rec.middle_name
            # if rec.lastname:
            #     name+= " "+ rec.lastname
            partner2 = self.search([('display_name', "=", rec.display_name), ('id', "!=", rec.id)], limit=1)
            if rec and partner2:
                # print('ccccccc',rec,partner2)
                _merge_method = self.sudo(2)._merge_method(rec, partner2)
                # print('_merge_method',_merge_method)
                # partner2.name=rec.name

    date = fields.Date('Partner since',
                       help="Date of activation of the partner or patient")
    alias = fields.Char('alias', size=64)
    ref = fields.Char('ID Number')
    is_person = fields.Boolean('Person',
                               help="Check if the partner is a person.")
    is_patient = fields.Boolean('Patient',
                                help="Check if the partner is a patient")
    is_doctor = fields.Boolean('Doctor',
                               help="Check if the partner is a doctor")
    is_institution = fields.Boolean('Institution',
                                    help="Check if the partner is a Medical Center")
    is_insurance_company = fields.Boolean('Insurance Company',
                                          help="Check if the partner is a Insurance Company")
    is_pharmacy = fields.Boolean('Pharmacy',
                                 help="Check if the partner is a Pharmacy")
    middle_name = fields.Char('Middle Name', size=128, help="Middle Name")
    lastname = fields.Char('Last Name', size=128, help="Last Name")
    insurance_ids = fields.One2many('medical.insurance', 'name', "Insurance")
    treatment_id = fields.Many2many('product.product',
                                    'treatment_insurance_company_relation',
                                    'treatment_id',
                                    'insurance_company_id', 'Treatment')

    _sql_constraints = [
        ('ref_uniq', 'unique (ref)',
         'The partner or patient code must be unique')
    ]

    @api.depends('name', 'lastname')
    def name_get(self):
        result = []
        for partner in self:
            name = partner.name
            if partner.middle_name:
                name += ' ' + partner.middle_name
            if partner.lastname:
                name += ' ' + partner.lastname
            result.append((partner.id, name))
        return result

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search(
                ['|', ('name', operator, name), ('ref_patient', operator, name)])
        if not recs:
            recs = self.search([('name', operator, name)])
        return recs.name_get()

    def get_user_name(self):
        return self.name