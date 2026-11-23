# -*- coding: utf-8 -*-
from odoo import fields, models, api

class CleaningService(models.Model):
    _name = 'cleaning.service'
    _description = 'Cleaning Service'
    _order = 'id desc'

    room_id = fields.Many2one('hostel.room')

    start = fields.Datetime('Start Time')
    user_id = fields.Many2one('res.users')
    stage = fields.Selection([('new','New'),
                              ('assigned','Assigned'),
                              ('done','Done'),],
                             default='new')
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.user.company_id)

    def assign(self):
        for record in self:
            if not record.start:
                record.start = fields.Datetime.now()
            if not record.user_id:
                record.user_id = self.env.user.id
            record.stage = 'assigned'

    def complete(self):
        for record in self:
            record.stage = 'done'






    def _compute_display_name(self):
        if self.id and self.user_id:
            self.display_name = f"{self.id}-{self.user_id.name}"
        else:
            self.display_name = 'Draft'
