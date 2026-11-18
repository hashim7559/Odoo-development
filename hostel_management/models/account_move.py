# -*- coding: utf-8 -*-
from odoo import fields, models

class AccountMove(models.Model):
    """this class represent an account move in the hotel management"""
    _inherit = 'account.move'

    def action_post(self):
        '''
        this function describes the post action of an account move
        in their add some more aditional action to the post button in the
        invoice module
        '''
        res = super().action_post()
        print(self.partner_id.name)
        # self.action_print_pdf()
        # print(a)
        # attachment = self.action_send_and_print()
        # self.action_send_and_print()
        # print(attachment)
        # print(self)
        # email_value= { 'attachment_ids': attachment}

        template = self.env.ref('hostel_management.email_template_data')
        template.send_mail(self.id, force_send=True,)
        return res

    room_id = fields.Many2one('hostel.room')
