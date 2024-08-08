# Copyright (C) 2021 - WATTIO dev@wattio.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import ast, json
import logging
from datetime import datetime

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class Mailing(models.Model):
    _inherit = 'mailing.mailing'

    template_mail_id = fields.Many2one(
        comodel_name="mail.template",
        string="Email Template",
    )

    last_update_date = fields.Datetime(
        string="Data Update",
        help='Last time that State was updated',
        compute='compute_last_state_update',
        store=True,
    )

    body_html = fields.Html(
        string='Body converted to be send by mail',
        sanitize_attributes=False,
        compute="compute_body_html",
    )

    trigger = fields.Selection(
        string="Type Trigger",
        selection=[
            ("campaign_start", "Início da campanha"),
            ("message_opened", "Mensagem aberta"),
            ("message_clicked", "Mensagem clicada"),
            ("message_replied", "Mensagem respondida"),
            ("message_not_opened", "Mensagem não aberta"),
            ("message_not_replied", "Mensagem não respondida"),
        ],
        default="campaign_start",
    )

    trigger_mailing_id = fields.Many2one(
        comodel_name="mailing.mailing",
        string="Activity Trigger",
    )

    trigger_qty_time = fields.Integer(
        string="Quantidade para acionar"
    )

    trigger_type_time = fields.Selection(
        string="Type Time Trigger",
        selection=[
            ("minutes", "Minutos(s)"),
            ("hours", "Hora(s)"),
            ("days", "Dias(s)"),
        ],
        default="minutes"
    )

    sequence = fields.Integer(
        string='Sequence',
        default=lambda self:
        self.env['ir.sequence'].next_by_code('increment_sequence')
    )

    ir_actions_server_id = fields.Many2one(
        comodel_name='ir.actions.server',
        string='Server action',
    )

    state = fields.Selection(
        selection_add=[
            ('stopped', 'Stopped')
        ],
        ondelete={'stopped': 'set default'}
    )

    #
    # Campos para configurar o modelo das atividades já que portamos o campo
    # para a utm.campaign
    #
    mailing_model_real = fields.Char(related='campaign_id.mailing_model_real')

    mailing_model_id = fields.Many2one(related='campaign_id.mailing_model_id')

    mailing_model_name = fields.Char(related='campaign_id.mailing_model_name')

    mailing_domain = fields.Char(compute='compute_mailing_domain', store=True)

    contact_list_ids = fields.Many2many(related='campaign_id.contact_list_ids')

    crm_stage_id = fields.Many2one(
        comodel_name="crm.stage"
    )

    proposal_state = fields.Selection(
        string='Proposal State',
        selection=[
            ('draft', 'Lead'),
            ('register', 'Aguardando Finalização do Cadastro'),
            ('documents-send', 'Aguardando envio de Documentos'),
            ('validate-doc', 'Aguardando Aprovação de Documentos'),
            ('docs-approves', 'Aguardando Envio para Assinatura'),
            ('sign-doc-client', 'Aguardando Assinatura de Contratos'),
            ('sign-doc-admin', 'Aguardando Assinatura da Cooperativa'),
            ('done', 'Ativo'),
            ('refused-doc', 'Aguardando Reenvio de Documento Recusado'),
            ('canceled', 'Cancelado'),
        ]
    )

    campaign_type = fields.Selection(
        string='Tipo de Campanha',
        selection=[
            ("active", "Campanha Ativa"),
            ("passive", "Campanha Passiva"),
        ],
        default="active",
    )

    total = fields.Integer(compute="_compute_total")

    @api.model
    def _process_mass_mailing_queue(self):
        """ Metodo disparado pelo cron """
        self._process_mass_mailing_queue_active()
        self._process_mass_mailing_queue_passive()

    def _process_mass_mailing_queue_active(self):
        _logger.info("_process_mass_mailing_queue_active")

        mass_active_mailing = self.search([
            ('campaign_id.campaign_type', '=', 'active'),
            ('state', 'in', ('in_queue', 'sending')),
            '|',
            ('schedule_date', '<', fields.Datetime.now()),
            ('schedule_date', '=', False)]
        )

        for mass_mailing in mass_active_mailing:

            user = mass_mailing.write_uid or self.env.user
            mass_mailing = mass_mailing.with_context(
                **user.with_user(user).context_get())

            if len(mass_mailing._get_remaining_recipients()) > 0:
                mass_mailing.state = 'sending'
                mass_mailing.action_send_mail()
            else:
                mass_mailing.write({
                    'state': 'done',
                    'sent_date': fields.Datetime.now(),
                    # send the KPI mail only if it's the first sending
                    'kpi_mail_required': not mass_mailing.sent_date,
                })

        mailings = self.env['mailing.mailing'].search([
            ('kpi_mail_required', '=', True),
            ('state', '=', 'done'),
            ('sent_date', '<=', fields.Datetime.now() - relativedelta(days=1)),
            ('sent_date', '>=', fields.Datetime.now() - relativedelta(days=5)),
        ])
        if mailings:
            mailings._action_send_statistics()

    def _compute_total(self):
        for mass_mailing in self:
            if mass_mailing.mailing_model_real:
                total = self.env[mass_mailing.mailing_model_real].search_count(mass_mailing._parse_mailing_domain())
                if mass_mailing.contact_ab_pc < 100:
                    total = int(total / 100.0 * mass_mailing.contact_ab_pc)
                mass_mailing.total = total
            else:
                mass_mailing.total = 0

    def _process_mass_mailing_queue_passive(self):
        _logger.info("_process_mass_mailing_queue_passive")

        mass_passive_mailing = self.search([
            ('campaign_id.campaign_type', '=', 'passive'),
            ('state', 'in', ('in_queue', 'sending')),
            '|',
            ('schedule_date', '<', fields.Datetime.now()),
            ('schedule_date', '=', False)]
        )

        mass_passive_mailing_proposal = mass_passive_mailing.filtered(lambda record: record.mailing_model_real == "proposal")
        mass_passive_mailing_lead = mass_passive_mailing.filtered(lambda record: record.mailing_model_real == "crm.lead")
        self._process_mass_mailing_queue_passive_proposal(mass_passive_mailing_proposal)
        self._process_mass_mailing_queue_passive_lead(mass_passive_mailing_lead)

    def _process_mass_mailing_queue_passive_proposal(self, mass_passive_mailing_proposal):
        for mass_mailing in mass_passive_mailing_proposal:
            already_mailed = self.env['mailing.trace'].search([
                ('model', '=', 'proposal'),
                ('mass_mailing_id', '=', mass_mailing.id)
            ])

            formated_mailing_domain = mass_mailing.mailing_domain.replace('"&",', "")
            ast_deserilized_mailing_domain = ast.literal_eval(formated_mailing_domain)
            ast_querys = tuple(tuple(query) for query in ast_deserilized_mailing_domain)

            record_ids = self.env["proposal"].search([
                ('id', 'not in', already_mailed.mapped("res_id")),
                ('state', '=', mass_mailing.proposal_state),
                *ast_querys
            ])

            record_ids = record_ids.filtered(lambda record: record.day_close >
                                                  mass_mailing.convert_trigger_qty_time_to_minutes())._ids
            if record_ids:
                mass_mailing.action_send_mail(res_ids=record_ids)

            mass_mailing.state = 'sending'

    def _process_mass_mailing_queue_passive_lead(self, mass_passive_mailing_lead):
        for mass_mailing in mass_passive_mailing_lead:
            already_mailed = self.env['mailing.trace'].search([
                ('model', '=', 'crm.lead'),
                ('mass_mailing_id', '=', mass_mailing.id),

            ])

            formated_mailing_domain = mass_mailing.mailing_domain.replace('"&",', "")
            ast_deserilized_mailing_domain = ast.literal_eval(formated_mailing_domain)
            ast_querys = tuple(tuple(query) for query in ast_deserilized_mailing_domain)

            record_ids = self.env["crm.lead"].search([
                ('id', 'not in', already_mailed.mapped("res_id")),
                ('stage_id', '=', mass_mailing.crm_stage_id.id),
                *ast_querys
            ])

            #TODO Verificar filtro
            # record_ids = record_ids.filtered(lambda record: record.day_close >
            #                                                 mass_mailing.convert_trigger_qty_time_to_minutes())._ids
            if record_ids:
                mass_mailing.action_send_mail(res_ids=record_ids)

            mass_mailing.state = 'sending'

    def convert_trigger_qty_time_to_minutes(self):
        if self.trigger_type_time == "minutes":
            return float(self.trigger_qty_time)

        if self.trigger_type_time == "hours":
            return float(self.trigger_qty_time * 60)

        if self.trigger_type_time == "days":
            return float(self.trigger_qty_time * 1440)

    @api.depends("template_mail_id")
    def compute_body_html(self):
        for record in self:
            if record.template_mail_id:
                if record.template_mail_id.body_html:
                    record.body_html = record.template_mail_id.body_html
                else:
                    record.body_html = ""
            else:
                record.body_html = ""

    @api.depends('campaign_id.mailing_domain')
    def compute_mailing_domain(self):
        """
        This function checks if the field mailing_domain does exist in the utm.campaign module and
        ,if so, sets de mailing.mailing_domain to this value.
        If utm.campaign.mailing_domain is == [], the ._get_default_mailing_domain() method ios called
        """
        if self.campaign_id.mailing_domain == "[]":
            self.mailing_domain = self._get_default_mailing_domain()
        else:
            self.mailing_domain = self.campaign_id.mailing_domain

    @api.onchange('template_mail_id')
    def _onchange_template_mail_id(self):
        """   """
        for record in self:
            if record.template_mail_id:
                record.body_html = record.template_mail_id.body_html
                record.subject = record.template_mail_id.subject
                record.email_from = self.env.company.email
            else:
                record.body_html = False
                record.subject = False
                record.email_from = False

    @api.onchange('name')
    def _onchange_name(self):
        """   """
        for record in self:
            if record.mailing_type != 'mail':
                record.subject = record.name
            else:
                record.email_from = self.env.company.email

    @api.depends('state')
    def compute_last_state_update(self):
        for record in self:
            record.last_update_date = datetime.now()
            record.campaign_id.is_all_activity_state_sent()

    # def _compute_statistics(self):
    #     try:
    #         obj_fields = [
    #             'scheduled', 'expected', 'ignored', 'sent',
    #             'delivered', 'opened', 'clicked', 'replied',
    #             'bounced', 'failed', 'received_ratio',
    #             'opened_ratio', 'replied_ratio', 'bounced_ratio'
    #         ]
    #         for obj in self:
    #             for field_name in obj_fields:
    #                 if getattr(obj, field_name) is None:
    #                     setattr(obj, field_name, 0)
    #
    #         return super(Mailing, self)._compute_statistics()
    #
    #     except Exception as e:
    #         _logger.exception(str(e))

    # def _get_remaining_recipients(self):
    #     res_ids = super(Mailing, self)._get_remaining_recipients()
    #
    #     if self.trigger_mailing_id:
    #         domain = [
    #             ('model', '=', self.mailing_model_real),
    #             ('res_id', 'in', res_ids),
    #             ('mass_mailing_id', '=', self.trigger_mailing_id.id)
    #         ]
    #         status_domain = get_status_domain(self.trigger, domain)
    #         if status_domain:
    #             tracking = self.env['mailing.trace'].search_read(status_domain, ['res_id'])
    #             missing_res_ids = {record['res_id'] for record in tracking}
    #             new_res_ids = [rid for rid in res_ids if rid in missing_res_ids]
    #             if new_res_ids is None:
    #                 new_res_ids = []
    #             return new_res_ids
    #         else:
    #             if res_ids is not None:
    #                 return res_ids
    #             else:
    #                 return []
    #     else:
    #         return res_ids

    # def action_create_activity(self):
    #     """   """
    #     return {'type': 'ir.actions.act_window_close'}
    #
    # def action_edit_activity(self):
    #     """   """
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'reload',
    #     }

# def get_status_domain(trigger, domain):
#     status_field = {
#         'message_opened': ('opened', '!=', False),
#         'message_clicked': ('clicked', '!=', False),
#         'message_replied': ('replied', '!=', False),
#         'message_not_opened': ('opened', '=', False),
#         'message_not_replied': ('replied', '=', False)
#     }
#     return AND([[status_field.get(trigger, False)],domain]) if status_field.get(trigger, False) else False
