from odoo import fields,models,api,_

class HostelStudent(models.Model):
    _name="hostel.student"
    _inherits = {'res.partner': 'partner_id'}
    _description = "Hostel Student"
    _rec_name = 'student_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    INVOICE_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]
    student_id = fields.Char(string="Student ID", required=True, copy=False, readonly=True, default= 'New')
    hostel_id = fields.Many2one(comodel_name="res.company", required=True, index=True, default=lambda self: self.env.company)
    partner_id = fields.Many2one("res.partner", required=True, ondelete='cascade')
    student_email = fields.Char( string="Student Email")
    student_phone = fields.Integer(string="Student Phone")
    student_address = fields.Text(string="Student Address")
    student_code = fields.Integer(string="Student Code")
    student_dob = fields.Datetime( string="Student DOB")
    student_age = fields.Integer( string="Student Age",compute='compute_student_age')
    room_id = fields.Many2one("hostel.room", string="Room")
    invoice_status = fields.Selection(selection=INVOICE_STATUS,string="Invoice Status")

    @api.onchange('student_dob')
    def compute_student_age(self):
        for record in self:
            if record.student_dob:
                year = record.student_dob.year
            else:
                year = 2026
            record.student_age =  fields.Date.today().year - year

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('student_id', _('New')) == _('New'):
                vals['student_id'] = self.env['ir.sequence'].next_by_code('hostel.student.sequence')
        return super(HostelStudent, self).create(vals_list)

