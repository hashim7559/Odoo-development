# -*- coding: utf-8 -*-
from odoo import fields, models,api, _, Command

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
                                     string="Facilities", tracking=1)
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
    student_count = fields.Integer(string="students in room",
                                   compute="_compute_student_count", default=0)
    room_status = fields.Selection(selection=[
                                                ("empty", "Empty"),
                                                ("partial", "Partial"),
                                                ("full", "Full")],
                                   string="Room Status", default="empty",
                                   compute="_compute_room_status", store=True)
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

    def monthly_invoice(self):
        print("hello world")
        for record in self:
            l=len(record.student_ids)
            print(l)
            print(record.student_ids[l-1].partner_id.id)
            for i in range(0,l):
                self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'partner_id': record.student_ids[i].partner_id.id,
                    'company_id': self.company_id.id,
                    'invoice_line_ids': [Command.create({
                        'product_id':self.product_id.id,
                        'price_unit':self.total_rent,})]
                })


