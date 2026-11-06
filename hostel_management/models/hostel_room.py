from odoo import fields, models,api, _

class HostelRoom(models.Model):
    _name = "hostel.room"
    _description = "Hostel Room"
    _rec_name = 'room_number'
    _inherit = ['mail.thread', 'mail.activity.mixin']



    room_number = fields.Char(string="Room Number", required=True, copy=False,
                              readonly=True, default= 'New')
    demo= fields.Char(string="Demo Room")
    room_type = fields.Selection(selection=[
                                        ('single', 'Single'),
                                        ('double', 'Double')],
                                        string="Room Type", default='single')
    bed_count = fields.Integer(string="Number of Bed")
    base_rent = fields.Monetary(string="Base Rent",
                                currency_field='currency_id')
    facilities_id = fields.Many2many('hostel.facility',
                                     string="Facilities")
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
        for vals in vals_list:
            if vals.get('room_number', _('New')) == _('New'):
                vals['room_number'] = (self.env['ir.sequence'].
                                       next_by_code('hostel.room.sequence'))
        return super(HostelRoom, self).create(vals_list)

