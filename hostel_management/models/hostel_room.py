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
    company_id = fields.Many2one(comodel_name="res.company", required=True,
                                 index=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name="res.currency",
                                  string="Currency",
                                  related="company_id.currency_id")

    room_status = fields.Selection(selection=[
                                                ("empty", "Empty"),
                                                ("partial", "Partial"),
                                                ("full", "Full")],
                                   string="Room Status", default="empty")


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
