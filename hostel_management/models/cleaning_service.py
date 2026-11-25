# -*- coding: utf-8 -*-
from odoo import fields, models, api

class CleaningService(models.Model):
    _name = 'cleaning.service'
    _description = 'Cleaning Service'
    _order = 'id desc'

    room_id = fields.Many2one('hostel.room')

    start = fields.Datetime('Start Time')
    user_id = fields.Many2one('res.users')
    stage = fields.Selection([('new','New'),
                              ('assigned','Assigned'),
                              ('done','Done'),],
                             default='new')
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.user.company_id)

    def assign(self):
        for record in self:
            if not record.start:
                record.start = fields.Datetime.now()
            if not record.user_id:
                record.user_id = self.env.user.id
            record.stage = 'assigned'
            record.room_id.activity_schedule(
                act_type_xmlid='hostel_management.mail_activity_data_cleaning',
                summary=f'cleaning service for {record.room_id.display_name}',
                user_id=record.user_id.id ,
                date_deadline=record.start ,
            )

    def complete(self):
        for record in self:
            record.stage = 'done'


    # def create(self,vals_list):
    #     print(vals_list)
    #     room= vals_list['room_id']
    #     rooms= self.env['hostel.room'].search([('id','=',room)])
    #     rooms.activity_schedule(
    #         act_type_xmlid='hostel_management.mail_activity_data_cleaning',
    #                        summary=f'cleaning service for {rooms.display_name}',
    #                        user_id=self.env.user.id,
    #                        date_deadline=vals_list['start'] if vals_list['start'] else fields.Date.today(),
    #                        )
    #     return super().create(vals_list)



    def _compute_display_name(self):
        if self.id and self.user_id:
            self.display_name = f"{self.id}-{self.user_id.name}"
        else:
            self.display_name = 'Draft'
