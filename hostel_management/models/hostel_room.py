# -*- coding: utf-8 -*-
from calendar import monthrange
from email.policy import default

from dateutil.relativedelta import relativedelta

from odoo import fields, models,api, _, Command

from odoo.exceptions import UserError

class HostelRoom(models.Model):
    '''
    It's a part of hostel management that consist details such as room_number,
    room_type,base_rent,and facilities. in side of that a def created that
    shows the sequence.
    '''
    _name = "hostel.room"
    _description = "Hostel Room"
    _rec_name = 'room_number'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    room_number = fields.Char(string="Room Number", required=True, copy=False,
                              readonly=True, default= 'New', )
    room_type = fields.Selection(selection=[
                                        ('single', 'Single'),
                                        ('double', 'Double')],
                                        string="Room Type", required=True,
                                        default='single', tracking=2)
    bed_count = fields.Integer(string="Number of Bed")
    base_rent = fields.Monetary(string="Base Rent",
                                currency_field='currency_id')
    facilities_id = fields.Many2many('hostel.facility',
                                     string="Facilities", tracking=1,
                                     ondelete='restrict')
    total_rent = fields.Monetary(string="Total Rent",
                                 currency_field='currency_id',
                                 compute='_compute_total_rent',
                                 inverse='_inverse_total_rent')
    company_id = fields.Many2one(comodel_name="res.company", required=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name="res.currency",
                                  string="Currency",
                                  related="company_id.currency_id")
    student_ids = fields.One2many(comodel_name="hostel.student",
                                  inverse_name="room_id", tracking=True,
                                  readonly=True,)
    cleaning_ids = fields.One2many(comodel_name="cleaning.service",
                                   inverse_name='room_id',)
    ribbon = fields.Boolean(default=True, compute='_compute_ribbon')
    student_count = fields.Integer(string="students in room",
                                   compute="_compute_student_count", default=0)
    room_status = fields.Selection(selection=[
                                                ("empty", "Empty"),
                                                ("partial", "Partial"),
                                                ("full", "Full")],
                                   string="Room Status", default="empty",
                                   compute="_compute_room_status", store=True)
    pending_amount = fields.Monetary(string="Pending Amount",
                                     currency_field='currency_id',
                                     compute='_compute_pending_amount')
    product_id = fields.Many2one(comodel_name="product.product",
                                 default = lambda self: self.env['product.product'].search([('id', '=',204)], limit=1))

    @api.depends('base_rent','total_rent','facilities_id')
    def _compute_total_rent(self):
        for record in self:
            record.total_rent = record.base_rent +sum(
                record.facilities_id.mapped('monthly_charge'))

    def _inverse_total_rent(self):
        for record in self:
            record.base_rent = record.total_rent - sum(
                record.facilities_id.mapped('monthly_charge'))

    @api.depends('student_ids')
    def _compute_student_count(self):
        self.student_count = len(self.student_ids)
        print(len(self.student_ids))


    @api.depends('bed_count','student_count')
    def _compute_room_status(self):
        if self.student_count ==0:
            self.room_status = "empty"
        elif self.student_count < self.bed_count:
            self.room_status = "partial"
        else:
            self.room_status = "full"

    @api.depends('student_ids')
    def _compute_pending_amount(self):
        for record in self:
            unpaid_invoices = self.env['account.move'].search([
                ('move_type', '=', 'out_invoice'),
                ('room_id', '=', record.id),
                ('status_in_payment', '!=' , 'paid'),
                ('status_in_payment', '!=' , 'in_payment')])

            record.pending_amount = sum(unpaid_invoices.mapped('amount_residual_signed'))


    @api.depends('cleaning_ids')
    def _compute_ribbon(self):
        if self.cleaning_ids:
            count =0
            for record in self.cleaning_ids:
                if record.stage == 'done':
                    count += 1
            if count == len(self.cleaning_ids):
                self.ribbon = True
            else:
                self.ribbon = False
        else:
            self.ribbon = True


    @api.model_create_multi
    def create(self, vals_list):
        '''
            this function consist sequence generation its uses the super also
        '''
        for vals in vals_list:
            if vals.get('room_number', _('New')) == _('New'):
                vals['room_number'] = (self.env['ir.sequence'].
                                       next_by_code('hostel.room.sequence'))
        return super(HostelRoom, self).create(vals_list)

    def cron_monthly_invoice(self):
        rooms = self.env['hostel.room'].search([('room_type', '!=', False)])
        for record in rooms:
            for student in record.student_ids:
                invoice = record.env['account.move'].search([
                    ('move_type', '=', 'out_invoice'),
                    ('partner_id', '=', student.partner_id.id),
                    ('room_id', '=', record.id), ])
                monthstart = fields.Date.today().replace(day=1)

                if not invoice:
                    record.call(student,record)
                else:
                    if invoice[0].invoice_date < monthstart:
                        record.call(student, record)


    def monthly_invoice(self):
        for record in self:
            count = 0
            for student in record.student_ids:
                invoice = record.env['account.move'].search([
                    ('move_type', '=', 'out_invoice'),
                    ('partner_id', '=', student.partner_id.id),
                    ('room_id', '=', record.id),])
                monthstart = fields.Date.today().replace(day=1)
                if not invoice:
                    record.call(student,record)
                else:
                    print(invoice[0].invoice_date)
                    if invoice[0].invoice_date < monthstart:
                        record.call(student,record)
                    else:
                        count +=1
            if count == len(record.student_ids):
                print(count)
                raise UserError("invoice's for the student's is already "
                                "generated for this month.")

    def call(self,student,record):
        day = monthrange(year=fields.Date.today().year,
                         month=fields.Date.today().month)[1]
        join_month = student.student_ids.joining.month
        today_month = fields.Date.today().month
        join_rent = day - student.student_ids.joining.day
        self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': student.partner_id.id,
            'company_id': record.company_id.id,
            'room_id': record.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [
                Command.create({
                    'product_id': record.product_id.id,
                    'price_unit': record.total_rent / day,
                    'quantity': day if join_month < today_month else join_rent,
                })
            ]
        })




    def room_invoices(self):
        '''
            It's an action button. this function that helps to redirect to
            the account move based on the sertain craitiria. they have one
            domain for listing only the related fields.
        '''
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        action['domain'] = [('room_id','=', self.id)]
        return action