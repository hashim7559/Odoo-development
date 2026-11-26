from odoo import fields, models, api

class MailActivity(models.Model):
    _inherit = 'mail.activity'

    cleaning_id = fields.Many2one('cleaning.service')