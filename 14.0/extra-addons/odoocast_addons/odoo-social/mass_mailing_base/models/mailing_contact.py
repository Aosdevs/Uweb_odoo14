from odoo import models


class MassMailingContact(models.Model):
    _inherit = 'mailing.contact'

    def add_contact_to_mailing_list(self):

        ctx = {
            "default_mailing_contact_ids":
                [(4, record.id) for record in self]
        }

        return {
            'name': 'Adicionar Contatos à Listas de E-mail existentes',
            'view_mode': 'form',
            'res_model': 'mailing.list.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': ctx
        }
