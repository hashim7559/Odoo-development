from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cleaning_tolerance = fields.Integer("Clean  ing Tolerance", config_parameter="cleaning_tolerance")