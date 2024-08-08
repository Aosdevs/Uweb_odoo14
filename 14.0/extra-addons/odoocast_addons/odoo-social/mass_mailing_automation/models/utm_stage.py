# Copyright (C) 2020 - SUNNIT dev@sunnit.com.br
# Copyright (C) 2021 - WATTIO dev@wattio.com.br
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class UtmStage(models.Model):
    """Stage for utm campaigns. """
    _inherit = 'utm.stage'

    fold = fields.Boolean(
        string="Kanban Folded?",
        default=False,
    )

    next_stage_id = fields.Many2one(
        string='Next Stage',
        comodel_name='utm.stage',
    )

    def unlink(self):
        stage_1 = self.env.ref("mass_mailing_automation.data_campaign_stage_1")
        stage_2 = self.env.ref("mass_mailing_automation.data_campaign_stage_2")
        stage_3 = self.env.ref("mass_mailing_automation.data_campaign_stage_3")
        stage_4 = self.env.ref("mass_mailing_automation.data_campaign_stage_4")
        stage_default = self.env.ref("utm.default_utm_stage")

        for record in self:
            if record in [stage_1, stage_2, stage_3, stage_4, stage_default]:
                raise ValidationError(f"Não é permetido excluir os Estágios:{record.name}")

        return super(UtmStage, self).unlink()
