# -*- coding: utf-8 -*-

from odoo import fields, models, api, _,Command
from odoo.exceptions import UserError


class HostelStudent(models.Model):
    '''
        It's a port of hostel management module. that consist of fields such as
        student_id, company_id, partner_id, age, room_id and invoice_status.
    '''
    _name = "hostel.student"
    _inherits = {'res.partner': 'partner_id'}
    _description = "Hostel Student"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_id = fields.Char(string="Student ID", required=True, copy=False,
                             readonly=True, default='New')
    company_id = fields.Many2one(comodel_name="res.company", required=True,
                                 default=lambda self: self.env.company)
    partner_id = fields.Many2one("res.partner", required=True,
                                 ondelete='cascade', readonly=True)
    dob = fields.Datetime(string="Student DOB")
    age = fields.Integer(string="Student Age")
    joining = fields.Date(String="Student Joining Date", readonly=True)

    room_id = fields.Many2one("hostel.room", string="Room",
                              readonly=True, copy=False)
    invoice_status = fields.Selection([('pending', 'Pending'),
                                       ('done', 'Done'),],
                                      string="Invoice Status",
                                      compute='_compute_invoice_status')
    payment_status = fields.Selection([('not_paid', 'Not paid'),
                                       ('paid', 'Paid'),],
                                      compute='_compute_payment_status')
    invoice_count = fields.Integer(string="Invoice Count",
                                   compute='_compute_invoice_count')
    currency_id = fields.Many2one(comodel_name="res.currency",
                                  string="Currency",
                                  related='company_id.currency_id')
    amount = fields.Monetary('Monthly amount', 'currency_id',
                             compute='_compute_monthly_amount')
    leave_request_ids = fields.One2many('leave.request',
                                        'student_id')

    @api.onchange('dob')
    def compute_student_age(self):
        '''
            this function consist of the age calaculation with using date of
            birth and today's date this function also consider month.
        '''
        for record in self:
            if not record.dob:
                year = fields.Date.today().year
                month = fields.Date.today().month
            else:
                year = record.dob.year
                month = record.dob.month

            age = fields.Date.today().year - year
            if month < fields.Date.today().month:
                record.age = age - 1
            else:
                record.age = age
            print(fields.Date.today().month)

    @api.depends()
    def _compute_invoice_count(self):
        for record in self:
            count = self.env['account.move'].search_count(
                [('partner_id', '=',record.partner_id.id),('move_type', '=', 'out_invoice')])
            record.invoice_count = count

    @api.depends('invoice_count')
    def _compute_monthly_amount(self):
        '''
        this compute method is used for calcualte remining rent the student
        need to pay wit using search amount_residual. why uses [0]-its helps
        to if multiple invoices takes fist invoice amount.
        '''
        for record in self:
            invoice = self.env['account.move'].search(
                [('partner_id', '=',record.partner_id.id),('move_type', '=', 'out_invoice')])
            if not invoice:
                record.amount = record.room_id.total_rent
            else:
                record.amount = invoice[0].amount_residual

    @api.depends('invoice_count')
    def _compute_invoice_status(self):
        for record in self:
            invoice= self.env['account.move'].search([
                ('partner_id', '=',record.partner_id.id),('move_type', '=', 'out_invoice')])
            if not invoice:
                record.invoice_status = False
            else:
                record.invoice_status = 'done'
                state = invoice.mapped('state')
                print(state)
                if 'draft' in state:
                    record.invoice_status = 'pending'

    @api.depends('invoice_count')
    def _compute_payment_status(self):
        for record in self:
            invoice = self.env['account.move'].search([
                ('partner_id', '=',record.partner_id.id),('move_type', '=', 'out_invoice')])
            if not invoice:
                record.payment_status = False
            else:
                record.payment_status = 'not_paid'
                status = invoice.mapped('status_in_payment')
                count=0
                for i in status:
                    if i =='paid' or i=='in_payment':
                        count += 1
                if count == len(status):
                    record.payment_status='paid'
                print(count)

    def _compute_display_name(self):
        for record in self:
            if record.partner_id:
                record.display_name = \
                    f"{record.student_id} - {record.partner_id.name}"
                # Why use f string becuse only str to str concatination posible +
            else:
                record.display_name = record.student_id + '-'

    def action_open_room_wizard(self):
        '''this fuction is used for the wizard calling purpose, it
        describes the view_mode also in there and describes context through
        value passing.'''
        return {
            'type': 'ir.actions.act_window',
            'name': 'list rooms available',
            'res_model': 'wizard.available.room',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_student_id': self.id},
        }

    def vacate(self):
        '''this function is used for vacate the student from room.'''
        self.cleaning_request()
        self.room_id = False
        self.joining = False


    def cleaning_request(self):
        print(self.room_id.bed_count)

        print(self.room_id.student_count)
        if self.room_id.student_count == 1:
            cleaning_service = self.env['cleaning.service'].search([
                ('room_id', '=', self.room_id.id),
                ('stage', '!=', 'done')])
            if not cleaning_service:
                self.env['cleaning.service'].create({
                    'room_id': self.room_id.id
                })
                self.room_id.message_post(body='cleaning request has been created.')
                print("cleaning request has been created")

    @api.ondelete(at_uninstall=True)
    def _delete_student(self):
        print("you cant delete student")
        for record in self:
            if record.room_id:
                raise UserError(f'The student {record.name} cant be delete. '
                                f'{record.name} is already assigned to the '
                                f'{record   .room_id.display_name} room.')

    def student_invoice(self):
        '''
        this function is used for redirecting into another action and through
        that pass a domain also.
        '''
        action = self.env["ir.actions.actions"]._for_xml_id(
            "account.action_move_out_invoice_type")
        action['domain'] = [('partner_id', '=', self.partner_id.id),('move_type', '=', 'out_invoice')]
        print(action)
        return action

    def grand_access(self):
        print(self.partner_id)
        self.env['res.users'].create({
            'partner_id': self.partner_id.id,
            'name': self.partner_id.name,
            'login': self.partner_id.email,
            'email': self.partner_id.email,
            'group_ids': [
                Command.set(self.env.ref('base.group_portal').ids)]
        })

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

class ResPartner(models.Model):
    '''this class represent res partner in the hotel management'''
    _inherit = 'res.partner'

    student_ids = fields.One2many('hostel.student', 'partner_id')
