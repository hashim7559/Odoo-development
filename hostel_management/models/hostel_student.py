# -*- coding: utf-8 -*-
from odoo import fields,models,api,_

class HostelStudent(models.Model):
    '''
        It's a port of hostel management module. that consist of fields such as
        student_id, company_id, partner_id, age, room_id and invoice_status.
    '''
    _name="hostel.student"
    _inherits = {'res.partner': 'partner_id'}
    _description = "Hostel Student"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    INVOICE_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]

    student_id = fields.Char(string="Student ID", required=True, copy=False,
                             readonly=True, default= 'New')
    company_id = fields.Many2one(comodel_name="res.company", required=True,
                                 index=True,
                                 default=lambda self: self.env.company)
    partner_id = fields.Many2one("res.partner", required=True,
                                 ondelete='cascade', readonly=True )
    dob = fields.Datetime( string="Student DOB")
    age = fields.Integer( string="Student Age")
    room_id = fields.Many2one("hostel.room", string="Room")
    invoice_status = fields.Selection(selection=INVOICE_STATUS,
                                      string="Invoice Status")

    @api.onchange('dob')
    def compute_student_age(self):
        '''
            this function consist of the age calaculation with using date of
            birth and today's date this function also consider month.
        '''
        for record in self:
            if not record.dob:
                year= fields.Date.today().year
                month= fields.Date.today().month
            else:
                year= record.dob.year
                month=record.dob.month

            age = fields.Date.today().year - year
            if month < fields.Date.today().month:
                record.age = age - 1
            else:
                record.age = age
            print(fields.Date.today().month)


    @api.model_create_multi
    def create(self, vals_list):
        '''
            this function consist sequence generation its uses the super also
        '''
        for vals in vals_list:
            if vals.get('student_id', _('New')) == _('New'):
                vals['student_id'] = (self.env['ir.sequence'].
                                      next_by_code('hostel.student.sequence'))
        return super(HostelStudent, self).create(vals_list)

    @api.depends('student_id','partner_id')
    def _compute_display_name(self):
        for record in self:
            if record.partner_id :
                record.display_name = f"{record.student_id} - {record.partner_id.name}"
                #Why use f string becuse only str to str concatination posible +
            else:
                record.display_name = record.student_id + '-'
