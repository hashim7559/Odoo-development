#
from odoo import fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super().action_post()
        print("Hyy")
        print(self.partner_id.name)
        template = self.env.ref('hostel_management.email_template_data')
        template.send_mail(self.id, force_send=True)
        return res

    room_id = fields.Many2one('hostel.room')