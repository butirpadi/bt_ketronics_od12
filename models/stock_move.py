from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    pack_qty = fields.Float(
        'Packing', compute='_compute_pack_weight', store=True)
    gross_weight = fields.Float(
        'Gross Weight', compute='_compute_pack_weight', store=True, default=0.00)
    net_weight = fields.Float(
        'Net Weight', compute="_compute_pack_weight", store=True, default=0.00)
    
    manufacture_order_id = fields.Many2one('mrp.production', string='M/Order')

    product_code = fields.Char('Product Code', related="product_id.default_code")

    @api.depends('quantity_done')
    def _compute_pack_weight(self):
        for rec in self:
            rec.pack_qty = rec.quantity_done / \
                rec.product_id.qty_per_pack if rec.quantity_done > 0 else 0
            rec.net_weight = rec.quantity_done * rec.product_id.weight
            rec.gross_weight = rec.net_weight + \
                (rec.product_id.pack_weight * rec.pack_qty)
