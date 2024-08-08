# Copyright (C) 2021 - WATTIO dev@wattio.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime

from ast import literal_eval
from odoo.addons.mass_mailing.models.mailing import \
    MASS_MAILING_BUSINESS_MODELS
from odoo.addons.mass_mailing_automation.tools import helpers

from odoo import fields, models, api
from odoo.exceptions import AccessDenied, ValidationError
from odoo.tools.translate import _

MASS_MAILING_BUSINESS_MODELS.remove('mailing.contact')
MASS_MAILING_BUSINESS_MODELS.remove('res.partner')

class UtmCampaign(models.Model):
    _inherit = 'utm.campaign'

    campaign_type = fields.Selection(
        string='Tipo de Campanha',
        selection=[
            ("active", "Campanha Ativa"),
            ("passive", "Campanha Passiva"),
        ],
        default="active",
    )
    #
    # Campos portados do mailing para utm.campaign para
    # identificar o alvo da campanha
    #
    mailing_model_real = fields.Char(
        string='Recipients Real Model',
        compute='_compute_model',
        default='crm.lead',
        required=True
    )

    mailing_model_id = fields.Many2one(
        string='Recipients Model',
        comodel_name='ir.model',
        domain=[('model', 'in', MASS_MAILING_BUSINESS_MODELS)],
        default=lambda self: self.env.ref('mass_mailing.model_mailing_list').id
    )

    mailing_model_name = fields.Char(
        related='mailing_model_id.model',
        string='Recipients Model Name',
        readonly=True,
        related_sudo=True
    )

    mailing_domain = fields.Char(
        string='Domain',
        default=[],
        readonly=False, store=True
    )

    contact_list_ids = fields.Many2many(
        comodel_name='mailing.list',
        relation='mass_utm_campaign_list_rel',
        string='Mailing Lists',
        copy=True,
    )

    stage_id = fields.Many2one(
        string='Stage',
        comodel_name='utm.stage',
        ondelete='restrict',
        required=True,
        compute='compute_stage',
        inverse='inverse_compute_stage',
        store=True,
    )

    use_related_campaign = fields.Boolean(
        string="Use Contacts from other Campaign",
        default=False,
    )

    trigger_related_campaign = fields.Selection(
        string="Trigger Filter",
        selection=[
            ("message_opened", "Mensagem aberta"),
            ("message_clicked", "Mensagem clicada"),
            ("message_replied", "Mensagem respondida"),
            ("message_not_opened", "Mensagem não aberta"),
            ("message_not_replied", "Mensagem não respondida"),
        ],
        default="message_replied",
    )

    # Stage Date control
    start_date = fields.Datetime(
        string="Campanha Iniciada em: ",
    )

    stop_date = fields.Datetime(
        string="Campanha encerrada em: ",
    )

    sent_date = fields.Datetime(
        string="Campanha enviada em: ",
    )

    schedule_date = fields.Datetime(
        string="Campanha agendada para: ",
    )
    # State for control
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('in_queue', 'In Queue'),
            ('sending', 'Sending'),
            ('done', 'Sent'),
            ('stopped', 'Stopped'),
        ],
        string='Status',
        default='draft',
        required=True,
        copy=False,
    )

    @api.depends('mailing_model_id', 'mailing_model_name')
    def _compute_model(self):
        """ Método do CORE para definir modelo real"""
        for record in self:
            record.mailing_model_real = \
                (record.mailing_model_name != 'mailing.list') and \
                record.mailing_model_name or 'mailing.contact'

    @api.depends("start_date", "stop_date", "sent_date", "schedule_date")
    def compute_stage(self):
        stage = self.env.ref("utm.default_utm_stage")
        for record in self:
            # Stage Stopped
            if record.stop_date:
                stage = self.env.ref("mass_mailing_automation.data_campaign_stage_4", False)
                self.reset_all_date()
            # Stage Scheduled
            elif record.schedule_date:
                stage = self.env.ref("mass_mailing_automation.data_campaign_stage_1", False)

            # Stage New
            elif not record.start_date:
                stage = self.env.ref("utm.default_utm_stage", False)

            # Stage Sending
            elif record.start_date and not record.sent_date:
                stage = self.env.ref("mass_mailing_automation.data_campaign_stage_2", False)

            # Stage Sent
            elif record.sent_date:
                stage = self.env.ref("mass_mailing_automation.data_campaign_stage_3", False)

            record.stage_id = stage

    def inverse_compute_stage(self):
        # Allow user to change campaign_stage in the UI

        # User drags campaign card to the NEW Stage
        if self.stage_id == self.env.ref("utm.default_utm_stage"):
            self.reset_all_date()

        # User drags campaign card to the SCHEDULED Stage
        if self.stage_id == self.env.ref("mass_mailing_automation.data_campaign_stage_1"):
            self.raise_schedule_warning()

        # User drags campaign card to the STOPPED Stage
        if self.stage_id == self.env.ref("mass_mailing_automation.data_campaign_stage_4"):
            self.inverse_action_stop_campaign()

    def reset_all_date(self):
        self.start_date = None
        self.sent_date = None
        self.stop_date = None

    def is_all_activity_state_sent(self):
        for activity in self.mailing_activities_ids:
            if activity.state != 'done':
                return

        self.sent_date = datetime.datetime.now()

    def next_stage(self):
        """
        This function checks if the variable set_next_stage does exists and ,if so,
        sets stage_id to the value of set_next_stage, else the function search for
        the next stage based in the sequence variable of utm.stage ans sets stage_id
        to this value
        """
        if self.stage_id.next_stage_id:
            self.stage_id = self.stage_id.next_stage_id
        else:
            sequence = self.stage_id.sequence

            next_stage = self.env['utm.stage'].search([
                ("sequence", ">", sequence)
            ], limit=1)

            if next_stage:
                self.stage_id = next_stage

    def raise_schedule_warning(self):
        raise AccessDenied(f"Para agendar a campanha {self.name} clique em seu card e va ate a opçao 'schedule' ")

    def prepare_action_wizard_mailing(self, type):
        context = dict(self._context or {})
        context.update({
            'default_mailing_type': type,
            'search_default_assigned_to_me': 1,
            'search_default_campaign_id': self.id,
            'default_user_id': self.env.user.id,
            'mailing_sms': True,
            'default_campaign_id': self.id,
            'default_campaign_type': self.campaign_type,
            'action_create_activity': True,
            'default_mailing_model_name': self.mailing_model_name,
        })

        if type == 'whatsapp':
            name = f"New Activity using {type.capitalize()}"
        elif type == 'sms':
            name = f"New Activity using {type.upper()}"
        else:
            name = "New Activity using E-mail"

        return {
            'name': name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mailing.mailing',
            'view_id': self.env.ref('mass_mailing_automation.mailing_mailing_view_form').id,
            'target': 'new',
            'context': context,
        }

    def action_wizard_mailing_whatsapp(self):
        return self.prepare_action_wizard_mailing('whatsapp')

    def action_wizard_mailing_sms(self):
        return self.prepare_action_wizard_mailing('sms')

    def action_wizard_mailing_mail(self):
        return self.prepare_action_wizard_mailing('mail')

    def action_schedule_campaign(self):
        action = self.env.ref('mass_mailing_automation.model_utm_campaign_schedule_date').read()[0]

        return {
            'name': action['name'],
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'utm.campaign.schedule.date',
            'view_id': self.env.ref('mass_mailing_automation.mass_mailing_schedule_date_view_form').id,
            'target': 'new',
            'context': dict(self.env.context, default_utm_campaign_id=self.id)
        }

    def action_start_campaign(self):
        """ Inicio de campanha """
        if not self.campaign_type:
            raise ValidationError(_('You must set up a campaign type.'))

        if not self.mailing_activities_ids:
            raise ValidationError(_('You must set up at least one activity '
                                    'to start this campaign.'))

        start_activity_ids = self.mailing_activities_ids.filtered(
            lambda m: m.trigger == 'campaign_start')

        for activity in start_activity_ids:
            activity.action_put_in_queue()

        self.start_date = datetime.datetime.now()

    def inverse_action_stop_campaign(self):
        for activity in self.mailing_activities_ids:
            activity.state = "stopped"
            activity.schedule_date = False

        self.reset_all_date()

    def action_stop_campaign(self):
        for activity in self.mailing_activities_ids:
            activity.state = "stopped"
            activity.schedule_date = False
        # Update stop_date to call compute_stage(self):
        self.stop_date = datetime.datetime.now()

    # @staticmethod
    # def get_scheduled(mailing_id, start_date=False):
    #     scheduled = fields.Datetime.now() if not start_date else start_date
    #     return helpers.define_time_trigger(mailing_id, scheduled)

    #
    # def set_children_activity_states(self, parent_activity, schedule=False):
    #     child_activity_ids = self.mailing_activities_ids.filtered(
    #         lambda m: m.trigger_mailing_id.id == parent_activity.id)
    #
    #     for child in child_activity_ids:
    #         if parent_activity.state == 'stopped':
    #             child.schedule_date = False
    #             child.state = 'stopped'
    #         elif child.state == 'draft':
    #             if not schedule:
    #                 parent_date = parent_activity.schedule_date or parent_activity.sent_date
    #             else:
    #                 parent_date = schedule
    #             child.schedule_date = self.get_scheduled(
    #                 child, start_date=parent_date)
    #             child.state = 'in_queue'
    #
    #         next_activity_ids = self.mailing_activities_ids.filtered(lambda m: m.trigger_mailing_id.id == child.id)
    #         if len(next_activity_ids) > 0:
    #             self.set_children_activity_states(child)

    # def filter_related_contacts(self, filter):
    #
    #     for mailing_list in self.related_campaign_id.contact_list_ids:
    #
    #         res_ids = mailing_list.contact_ids.ids
    #         domain = [
    #             ('model', '=', 'mailing.contact'),
    #             ('res_id', 'in', res_ids),
    #             ('campaign_id', '=', self.related_campaign_id.id)]
    #
    #         if filter == 'message_opened':
    #             search_domain = AND([domain, [('state', '=', 'opened')]])
    #         elif filter == 'message_clicked':
    #             search_domain = AND([domain, [('clicked', '!=', False)]])
    #         elif filter == 'message_replied':
    #             search_domain = AND([domain, [('state', '=', 'replied')]])
    #         elif filter == 'message_not_opened':
    #             search_domain = AND([
    #                 domain,
    #                 [('state', 'in', ['ignored', 'exception', 'bounced'])]
    #             ])
    #         elif filter == 'message_not_replied':
    #             search_domain = AND([
    #                 domain, [('replied', '=', False), ('state', '!=', 'replied')]
    #             ])
    #         else:
    #             search_domain = domain
    #
    #         matched_trace = self.env['mailing.trace'].search_read(search_domain, ['res_id'])
    #         missing_res_ids = {record['res_id'] for record in matched_trace}
    #         filtered_res_ids = [rid for rid in res_ids if rid in missing_res_ids]
    #
    #         if len(filtered_res_ids) > 0:
    #             id_campaign = self.id.origin if not isinstance(self.id, int) else self.id
    #             mtype = _('Filtred:')
    #             if not id_campaign:
    #                 mtype = _('Related:')
    #                 id_campaign = self.related_campaign_id.id
    #             name_campaign = f"L{id_campaign} - {mtype} {mailing_list.name}"
    #             existing_mailing_list = self.env['mailing.list'].search([('name', 'like', name_campaign)], limit=1)
    #             if not existing_mailing_list:
    #                 new_mailing_list = self.env['mailing.list'].create({
    #                     'name': name_campaign,
    #                     'is_public': mailing_list.is_public,
    #                     'contact_ids': [(6, 0, filtered_res_ids)],
    #                 })
    #                 if new_mailing_list:
    #                     self.contact_list_ids = [(6, 0, [new_mailing_list.id])]
    #                     self.mailing_activities_ids.write({'contact_list_ids': [(6, 0, [new_mailing_list.id])]})
    #                     self.notify_user(
    #                         title=_("Contacts List Created"),
    #                         msg=_("The contact list was successfully created!"),
    #                         type='success'
    #                     )
    #             else:
    #                 update_contacts = existing_mailing_list.write({'contact_ids': [(6, 0, filtered_res_ids)]})
    #                 if update_contacts:
    #                     self.contact_list_ids = [(6, 0, [existing_mailing_list.id])]
    #
    #                     self.notify_user(
    #                         title=_("Contacts List Updated"),
    #                         msg=_(
    #                             "The contact list was updated with filtered contacts!"),
    #                         type='success'
    #                     )
    #         else:
    #             self.notify_user(
    #                 title=_("Attention"),
    #                 msg=_("No filter applied in contact list"),
    #                 type='error',
    #                 sticky=True
    #             )

    # def find_trigger_mailing_parent(self, new_campaign):
    #     updated_activities = []
    #     # clean scheduled date
    #     new_campaign.mailing_activities_ids.write({
    #         'schedule_date': False,
    #         'mailing_model_name': new_campaign.mailing_model_name,
    #         'mailing_model_id': new_campaign.mailing_model_id.id
    #     })
    #
    #     for activity in new_campaign.mailing_activities_ids:
    #
    #         if activity.id not in updated_activities:
    #
    #             updating_activity = activity
    #             old_activity = self.mailing_activities_ids.filtered(
    #                 lambda m: m.name in updating_activity.name)
    #             if len(old_activity) > 1:
    #                 old_activity = old_activity[0]
    #
    #             if activity.trigger == 'campaign_start':
    #                 wrong_activity_ids = new_campaign.mailing_activities_ids.filtered(
    #                     lambda m: m.trigger_mailing_id.id == old_activity.id)
    #
    #                 for fix_activity in wrong_activity_ids:
    #                     fix_activity.trigger_mailing_id = updating_activity.id
    #                     updated_activities.append(fix_activity.id)
    #             elif activity.trigger_mailing_id.id < activity.id:
    #                 copy_trigger_mailing = self.env['mailing.mailing'].search([
    #                     ('name', 'ilike', activity.trigger_mailing_id.name), ('campaign_id', '=', new_campaign.id)
    #                 ], limit=1)
    #                 activity.trigger_mailing_id = copy_trigger_mailing.id
    #                 updated_activities.append(activity.id)

    # def notify_user(self, title, msg, type, sticky=False):
    #     msg_data = {
    #         "message": msg, "title": title, "sticky": sticky
    #     }
    #     if type == 'success':
    #         self.env.user.notify_success(**msg_data)
    #     elif type == 'error':
    #         self.env.user.notify_warning(**msg_data)
    #     elif type == 'danger':
    #         self.env.user.notify_danger(**msg_data)

    # @api.returns('self', lambda value: value.id)
    # def copy(self, default=None):
    #     self.ensure_one()
    #
    #     default = dict(
    #         default or {},
    #         name=_('%s (copy)') % self.name,
    #         contact_list_ids=self.contact_list_ids.ids
    #     )
    #
    #     campaign = super(UtmCampaign, self).copy(default=default)
    #
    #     self.find_trigger_mailing_parent(campaign)
    #
    #     campaign._onchange_model_and_list()
    #     return campaign
