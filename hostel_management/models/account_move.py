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
        if self.room_id:
            print("hello12121")
            print(self.partner_id.name)
            template = self.env.ref('hostel_management.email_template_data')
            template.send_mail(self.id, force_send=True,)
        return res

    room_id = fields.Many2one('hostel.room')
