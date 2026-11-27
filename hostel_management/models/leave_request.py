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
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.user.company_id)


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
        '''
        this function used to clean the leave request.
        this function is called when the leave request is approved.
        if only one student -> call create_request.
        else find all request in that room mapp->check all student in leave
        on one day -> call create_request.
        '''
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
        '''
        this function is called by previouse function.
        check if the ahe cleaning in that room-> check with tolerence ->
        create new cleaning request.
        else not have request -> create new cleaning request.
        '''
        tolerance = self.env['ir.config_parameter'].sudo().get_int('cleaning_tolerance')
        cleaning = self.env['cleaning.service'].search([('room_id', '=',
                                                         self.room_id.id)])
        count = 0
        if cleaning:
            for record in cleaning:
                after = record.start.date() + relativedelta(days=tolerance)
                before = record.start.date() - relativedelta(days=tolerance)
                if not before <= date <=after:
                    count += 1
        else:
            self.env['cleaning.service'].create({
                'room_id': self.student_id.room_id.id,
                'start': date,
                'company_id': self.company_id.id,
            })
            print("cleaning request approved form leave request")

        if count == len(cleaning):
            self.env['cleaning.service'].create({
                'room_id': self.student_id.room_id.id,
                'start': date,
                'company_id': self.company_id.id,
            })
            print("cleaning request approved form leave request")

