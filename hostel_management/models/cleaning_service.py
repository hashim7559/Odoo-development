# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from datetime import datetime

from odoo import fields, models, api,Command

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
                cleaning_id= record.id
            )

    def complete(self):
        for record in self:
            record.stage = 'done'
            asd = record.env['mail.activity'].search([('cleaning_id', '=', record.id)])
            print(asd)
            print(asd.state)
            asd.action_done()
            print(asd.state)


    def create(self,vals_list):
        res = super().create(vals_list)
        print(12121212)
        print(vals_list)
        tolerance = self.env['ir.config_parameter'].sudo().get_int('cleaning_tolerance')
        cleaning = self.env['cleaning.service'].search([
                                        ('room_id', '=',vals_list['room_id'])])
        for service in cleaning:
            tolerance_date = service.start.date() + relativedelta(days=tolerance)
            print(1212121212,tolerance_date)
            start = vals_list['start']
            print(start)
            st = datetime.strptime('start', '%yyyy-%mm-%dd %H:%M:%S').date()
            print(st)
            # if tolerance_date>start:
            #     print(123212)
        print(cleaning)
        return res

    def _compute_display_name(self):
        if self.id and self.user_id:
            self.display_name = f"{self.id}-{self.user_id.name}"
        else:
            self.display_name = 'Draft'
