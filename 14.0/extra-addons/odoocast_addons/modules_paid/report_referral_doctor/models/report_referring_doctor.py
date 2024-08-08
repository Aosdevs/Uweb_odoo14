# -*- coding: utf-8 -*-


from odoo import _, api, fields, models


class ReferralDoctor(models.AbstractModel):
    _name = 'report.report_referral_doctor.excel_report_referral_doctor'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        for obj in partners:
            report_name = obj.name
            # One sheet by partner
            sheet = workbook.add_worksheet('Referral Doctor Commission')
            format0 = workbook.add_format({'font_size': 15, 'align': 'center'})
            format1 = workbook.add_format(
                {'font_size': 15, 'align': 'center', 'bold': True, 'bg_color': '#D5D5D5', 'color': 'black',
                 'border': 2})
            format2 = workbook.add_format(
                {'font_size': 13, 'align': 'center', 'bold': True,
                 'border': 1})
            format10 = workbook.add_format({'align': 'center', 'bold': True, 'bg_color': '#FF6600', 'border': 5})
            format3 = workbook.add_format(
                {'align': 'center', 'bold': True, 'bg_color': '#4CE400', 'color': 'black', 'border': 5})
            row = 1
            if obj.referring_doctor_id:

                patients = self.env['medical.patient'].sudo().search(
                    [('referring_doctor_idd', '=', obj.referring_doctor_id.id)])
                medical_teeth_treatments = self.env['medical.teeth.treatment'].sudo().search(
                    [('patient_id', 'in', patients.ids), ('state', '=', 'completed'), ('completion_date', '>=', obj.date_from),
                     ('completion_date', '<=', obj.date_to)])
                if medical_teeth_treatments:
                    sheet.set_column(row, 1, 40)
                    sheet.set_column(row, 2, 100)
                    sheet.set_column(row, 3, 40)
                    sheet.set_column(row, 4, 20)
                    sheet.set_column(row, 5, 30)
                    sheet.set_column(row, 6, 20)
                    sheet.set_column(row, 7, 20)
                    sheet.write(row, 1, 'Referral Doctor', format1)
                    sheet.write(row, 2, 'Patient', format1)
                    sheet.write(row, 3, 'Completed Service', format1)
                    sheet.write(row, 4, 'Service Amount', format1)
                    sheet.write(row, 5, 'Completed By', format1)
                    sheet.write(row, 6, 'Commission %', format1)
                    sheet.write(row, 7, 'Commission Amount', format1)
                for medical in medical_teeth_treatments:
                    sheet.set_column(row, 1, 40)
                    sheet.set_column(row, 2, 100)
                    sheet.set_column(row, 3, 40)
                    sheet.set_column(row, 4, 20)
                    sheet.set_column(row, 5, 30)
                    sheet.set_column(row, 6, 20)
                    sheet.set_column(row, 7, 20)
                    row+=1
                    commission = 0
                    amount = 0
                    if obj.referring_doctor_id == medical.dentist :
                        commission = obj.self_commission
                    else:
                        commission = obj.other_commission
                    print('commission',commission)
                    amount = medical.net_amount * commission /100
                    sheet.write(row, 1, obj.referring_doctor_id.name, format2)
                    sheet.write(row, 2, str(medical.patient_id.patient_id) + ' - ' + str(medical.patient_id.partner_id.name), format2)
                    sheet.write(row, 3, medical.description.name, format2)
                    sheet.write(row, 4, medical.net_amount, format2)
                    sheet.write(row, 5, medical.dentist.name, format2)
                    sheet.write(row, 6, str(commission) + ' %' , format2)
                    sheet.write(row, 7, amount, format2)


