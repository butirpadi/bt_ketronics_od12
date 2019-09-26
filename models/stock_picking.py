from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sender_by = fields.Char('Sender by')
