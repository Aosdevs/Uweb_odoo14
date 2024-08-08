from odoo import http
from odoo.addons.web.controllers.main import ReportController, request


class ReportController(ReportController):

    @http.route(['/report/is_open_print_dialog'], type='json', auth="user")
    def is_open_print_dialog(self, report_ref):
        ir_actions_report_env = request.env['ir.actions.report']
        if isinstance(report_ref, int):
            report_action =\
                ir_actions_report_env.sudo().browse(report_ref)
        else:
            report_action =\
                ir_actions_report_env._get_report_from_name(report_ref)
        return report_action.is_open_print_dialog()
