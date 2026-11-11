# -*- coding: utf-8 -*-
from odoo import fields, models,_
class AvailableRoom(models.TransientModel):
    '''
        this is a wizard model that consist of the room model data the warden
        can choose the student, they have option like allot room once they
        click that autopopulate the bellow fields such as student_id,
        room_id, room_type,total_rent, room status and thy also able to give
        data to room_id field and joining field.
    '''
    _name = 'wizard.available.room'
    _description = 'Available Room'

    room_id = fields.Many2one('hostel.room',string='Room number',
                              domain="[('room_status','in',['empty','partial'])]"
                              ,required=True)
    student_id = fields.Many2one('hostel.student',string='Student',
                                 readonly=True)
    joining = fields.Date(string='Joining Date',default=fields.Date.today())
    room_type = fields.Selection(selection=[
                                            ('single', 'Single'),
                                            ('double', 'Double')],
                                 related='room_id.room_type')
    bed_count = fields.Integer(string='Bed count', related='room_id.bed_count')
    currency_id = fields.Many2one(related='room_id.currency_id')
    total_rent = fields.Monetary(string='Base rent',
                                 currency_field='currency_id',
                                 related='room_id.total_rent')
    room_status = fields.Selection(selection=[("empty", "Empty"),
                                                ("partial", "Partial"),
                                                ("full", "Full")],
                                   related='room_id.room_status')



    def confirm(self):
        '''
            this function describes to load room_id to the student model,
            load joining date to the joining date to the student model and
            post a massage in the room model chatter.
        '''
        self.student_id.room_id = self.room_id
        self.room_id.message_post(body=_(f"{self.student_id.name} "
                                           f"as been added"))
        self.student_id.joining = self.joining
