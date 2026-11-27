# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import fields, models, api,Command
from odoo.exceptions import UserError


class CleaningService(models.Model):
    '''
    this class is for cleaning service in hostel management.
    '''
    _name = 'cleaning.service'
    _description = 'Cleaning Service'
    _order = 'id desc'

    room_id = fields.Many2one('hostel.room')

    start = fields.Datetime('Start Time', default=fields.Date.today())
    user_id = fields.Many2one('res.users')
    stage = fields.Selection([('new','New'),
                              ('assigned','Assigned'),
                              ('done','Done'),],
                             default='new')
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.user.company_id)

    def assign(self):
        '''this method is for cleaning service in hostel management.
         used for assigning the employee to cleaning service.
         or self assigning employee to cleaning service.
         also triger the activity to hostel room.'''
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
        '''
        this method is for cleaning service in hostel management.
        used for when the service is done make as done.
        and also in activity in room.
        '''
        for record in self:
            record.stage = 'done'
            asd = record.env['mail.activity'].search([('cleaning_id', '=', record.id)])
            print(asd)
            print(asd.state)
            asd.action_done()
            print(asd.state)

    @api.onchange('start')
    def _check_start(self):
        for record in self:
            tolerance = self.env['ir.config_parameter'].sudo().get_int('cleaning_tolerance')
            service = self.env['cleaning.service'].search([('room_id', '=', record.room_id.id)])
            print(service)

            if service:
                for rec in service:
                    before = rec.start - relativedelta(days=tolerance)
                    after = rec.start + relativedelta(days=tolerance)
                    if before <= record.start <= after:
                        raise UserError(f'Thy have already cleaning request '
                                        f'on {rec.start}')

    def _compute_display_name(self):
        if self.id and self.user_id:
            self.display_name = f"{self.id}-{self.user_id.name}"
        else:
            self.display_name = 'Draft'
