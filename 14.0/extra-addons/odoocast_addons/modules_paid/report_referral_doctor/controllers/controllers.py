# -*- coding: utf-8 -*-
# from odoo import http


# class ReportAccountCustomer(http.Controller):
#     @http.route('/report_referral_doctor/report_referral_doctor/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_referral_doctor/report_referral_doctor/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_referral_doctor.listing', {
#             'root': '/report_referral_doctor/report_referral_doctor',
#             'objects': http.request.env['report_referral_doctor.report_referral_doctor'].search([]),
#         })

#     @http.route('/report_referral_doctor/report_referral_doctor/objects/<model("report_referral_doctor.report_referral_doctor"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_referral_doctor.object', {
#             'object': obj
#         })
