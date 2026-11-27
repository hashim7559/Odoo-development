# -*- coding: utf-8 -*-
from odoo import fields, models

class AccountMove(models.Model):
    """this class represent an account move in the hotel management"""
    _inherit = 'account.move'

    room_id = fields.Many2one('hostel.room')

    def action_post(self):
        '''
        this function describes the post action of an account move
        in their add some more aditional action to the post button in the
        invoice module
        '''
        #@todo:- self.env.ref and it's return type
        #@todo:- force send True and False, when send if it is false

        res = super().action_post()
        if self.room_id:
            print("hello12121")
            print(self.partner_id.name)
            template = self.env.ref('hostel_management.email_template_data')
            print(121212,template)
            template.send_mail(self.id, force_send=False,)
        return res

