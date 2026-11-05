from odoo import fields, models,api
from odoo.exceptions import UserError

class HostelFacility(models.Model):
    _name = 'hostel.facility'
    _description = 'Hostel Facility'
    _rec_name = 'facility_name'

    facility_name=fields.Char(string="Facility Name")
    hostel_id = fields.Many2one(comodel_name="res.company", required=True, index=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name="res.currency", string="Currency", compute='_compute_currency_id')
    monthly_charge = fields.Float(string="Monthly Charge")

    @api.depends('hostel_id')
    def _compute_currency_id(self):
        for record in self:
            record.currency_id = record.hostel_id.currency_id

    @api.constrains('monthly_charge')
    def _check_monthly_charge(self):
        for record in self:
            if record.monthly_charge == 0:
                raise UserError("Monthly Charge is zero its need more than 0")


