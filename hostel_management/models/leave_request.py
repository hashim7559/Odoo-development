# -*- coding: utf-8 -*-
from statistics import mode
from odoo import api,models,fields
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError



class LeaveRequest(models.Model):
    '''this model is for leave request model it consist of the entire leave
    management of the student that in the hostel'''
    _name= 'leave.request'
    _inherit = ['mail.thread','mail.activity.mixin']

    student_id=fields.Many2one('hostel.student','Student',
                               required=True, ondelete='cascade')
    room_id = fields.Many2one('hostel.room',related='student_id.room_id')

    from_date = fields.Date('From Date', default=fields.Date.today())
    to_date = fields.Date("To Date",
                          default = fields.Date.today()+relativedelta(days=+1))
    status = fields.Selection([('new','New'),
                               ('approved','Approved'),
                               ('rejected','Rejected'),
                               ('cancelled','Cancelled'),],
                              help="this field is define for the purpose of "
                                   "status of you leave request",
                              default='new', tracking=True)
    leave_type= fields.Selection([('home','Home Visit'),
                               ('medical','Medical'),
                               ('personal','Personal'),
                               ('other','Other'),], required=True)


    def _compute_display_name(self):
        for record in self:
            record.display_name = (f"{record.student_id.partner_id.name}-"
                                   f"({record.from_date})-({record.to_date})")

    def approve(self):
        '''this function used to approve the leave request'''
        if self.status != 'rejected':
            self.status = "approved"
            self.cleaning_request()

        else:
            raise UserError('''Rejected leave request can't be approve''')

    def reject(self):
        '''this function used to reject the leave request'''
        if self.status != 'approved':
            self.status = "rejected"
        else:
            raise UserError('''Approved leave request can't be rejected''')


    def cleaning_request(self):
        if len(self.room_id.student_ids) == 1:
            self.create_request(self.from_date)
        else:
            leave_requests = self.env['leave.request'].search([
                ('room_id', '=', self.room_id.id),
                ('status', '=', 'approved')
            ])
            dates=[]
            for leave_request in leave_requests:
                start=leave_request.from_date
                while (start <= leave_request.to_date):
                    dates.append(start)
                    start= (start +relativedelta(days=1))
            print(dates)
            print(mode(dates))
            count=dates.count(mode(dates))
            print(count)
            if len(self.room_id.student_ids) == count:
                self.create_request(mode(dates))

    def create_request(self,date):
        cleaning_service = self.env['cleaning.service'].search([
            ('room_id', '=', self.student_id.room_id.id),
            ('stage', '!=', 'done')])
        if not cleaning_service:
            self.env['cleaning.service'].create({
                'room_id': self.student_id.room_id.id,
                'start': date,
            })
            print("cleaning request approved form leave request")

