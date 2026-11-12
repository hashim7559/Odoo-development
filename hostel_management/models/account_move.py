#
from odoo import fields, models,_

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super().action_post()
        print("Hyy")
        print(self.partner_id.name)
        self.message_post(body=_(f"{self.partner_id.name} "
                                         f"s invoice as been posted."))
        template = self.env.ref('hostel_management.email_template_data')
        template.send_mail(self.id, force_send=True)
        return res