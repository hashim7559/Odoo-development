# -*- coding: utf-8 -*-
# It's a part of hostel management
from odoo import fields, models,api
from odoo.exceptions import UserError

class HostelFacility(models.Model):
    '''
        this class defines facility details such as facility name,
        monthly charge, etc. in side of that calculate whether the
        monthly charge is zero or not.
    '''
    _name = 'hostel.facility'
    _description = 'Hostel Facility'
    _rec_name = 'facility_name'

    facility_name=fields.Char(string="Facility Name")
    monthly_charge = fields.Monetary(string="Monthly Charge",
                                     currency_field='currency_id')
    company_id = fields.Many2one(comodel_name="res.company", required=True,
                                 index=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(comodel_name="res.currency",
                                  string="Currency",
                                  related="company_id.currency_id")



    @api.constrains('monthly_charge')
    def _check_monthly_charge(self):
        for record in self:
            if record.monthly_charge == 0:
                raise UserError("Monthly Charge is zero its need more than 0")