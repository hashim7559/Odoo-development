from odoo import fields, models,api, _

class HostelRoom(models.Model):
    _name = "hostel.room"
    _description = "Hostel Room"
    _rec_name = 'room_number'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    id = fields.Integer("Room Number", default=0, required=True)
    room_number = fields.Char(string="Room Number", required=True, copy=False, readonly=True, default= 'New')
    hostel_id = fields.Many2one(comodel_name="res.company", required=True, index=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency", compute='_compute_currency_id')
    room_type = fields.Selection(selection=[('single', 'Single'),('double', 'Double')], string="Room Type", default='single')
    bed_count = fields.Integer(string="Number of Bed")
    base_rent = fields.Integer(string="Base Rent")
    facilities_id = fields.Many2many('hostel.facility', string="Facilities")
    room_status = fields.Selection(  selection=[("empty", "Empty"),("partial", "Partial"),("full", "Full")], string="Room Status", default="empty")

    @api.depends('hostel_id')
    def _compute_currency_id(self):
        for record in self:
            record.currency_id = record.hostel_id.currency_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('room_number', _('New')) == _('New'):
                vals['room_number'] = self.env['ir.sequence'].next_by_code('hostel.room.sequence')
        return super(HostelRoom, self).create(vals_list)


