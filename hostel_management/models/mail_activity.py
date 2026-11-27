from odoo import fields, models, api

class MailActivity(models.Model):
    '''
    this class is used to create new cleaning_id into mail_activity.
    '''
    _inherit = 'mail.activity'

    cleaning_id = fields.Many2one('cleaning.service')
