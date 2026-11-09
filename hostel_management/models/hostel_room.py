# -*- coding: utf-8 -*-
from odoo import fields, models,api, _

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
                                 compute='_compute_total_rent')
    company_id = fields.Many2one(comodel_name="res.company", required=True,
                                 index=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name="res.currency",
                                  string="Currency",
                                  related="company_id.currency_id")
    student_ids = fields.One2many(comodel_name="hostel.student",
                                  inverse_name="room_id", tracking=True,)
    available = fields.Integer(string="students in room",
                               compute="compute_available")


    room_status = fields.Selection(selection=[
                                                ("empty", "Empty"),
                                                ("partial", "Partial"),
                                                ("full", "Full")],
                                   string="Room Status", default="empty",
                                   compute="_compute_room_status", store=True)

    @api.depends('base_rent','total_rent','facilities_id')
    def _compute_total_rent(self):
        for record in self:
            record.total_rent = (record.total_rent + record.base_rent +
                                 sum(record.facilities_id.mapped(
                                     'monthly_charge')))


    @api.depends('student_ids')
    def compute_available(self):
        self.available = len(self.student_ids)
        print(len(self.student_ids))


    @api.depends('bed_count','available')
    def _compute_room_status(self):
        if self.available ==0:
            self.room_status = "empty"
        elif self.available < self.bed_count:
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
