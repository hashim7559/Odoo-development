from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    '''
    this class in used to add cleaning_tolerance into res.config.settings.
    '''
    _inherit = "res.config.settings"

    cleaning_tolerance = fields.Integer("Clean  ing Tolerance",
                                        config_parameter="cleaning_tolerance")
