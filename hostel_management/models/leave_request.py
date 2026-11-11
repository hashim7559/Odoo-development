# -*- coding: utf-8 -*-
from odoo import api,models,fields
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class LeaveRequest(models.Model):
    '''this model is for leave request model it consist of the entire leave
    management of the student that in the hostel'''
    _name= 'leave.request'
    _inherit = ['mail.thread','mail.activity.mixin']

    student_id=fields.Many2one('hostel.student','Student',
                               required=True)

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
    @api.constrains('from_date','to_date')
    def _check_dates(self):
        for record in self:
            if record.from_date > record.to_date:
                raise UserError("Leave ending date not be lover than starting "
                                "date")

    def _compute_display_name(self):
        if self.student_id.partner_id.name:
            self.display_name = (f"{self.student_id.partner_id.name}-"
                                 f"({self.from_date})-({self.to_date})")
        else:
            self.display_name = f"({self.from_date})-({self.to_date})"

    def approve(self):
        '''this function used to approve the leave request'''
        if self.status != 'rejected':
            self.status = "approved"
        else:
            raise UserError('''Rejected leave request can't be approve''')

    def reject(self):
        '''this function used to reject the leave request'''
        if self.status != 'approved':
            self.status = "rejected"
        else:
            raise UserError('''Approved leave request can't be rejected''')
