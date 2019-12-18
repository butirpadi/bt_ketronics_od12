from odoo import api, fields, models, _


class ButirSalesReportWizard(models.TransientModel):
    _name = 'butir.sales.report.wizard'
    _description = 'Sales Report / Laporan penjualan'

    name = fields.Char(string='Name', default="Sales Report")
    date_start = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    invoice_ids = fields.Many2many(
        comodel_name='account.invoice',
        relation='account_invoice_sales_report_rel',
        column1='report_id',
        column2='invoice_id',
        string='Invoices'
    )

    def action_submit(self):
        all_invoices = self.env['account.invoice'].search(
            ['&', '&', '&',
             ('type', '=', 'out_invoice'),
             ('state', 'in', ['open', 'paid']),
             ('date_invoice', '>=', self.date_start),
             ('date_invoice', '<=', self.date_to),
             ])
        
        self.write({
            'invoice_ids': [(6, 0, all_invoices.ids)]
        })

        # # show current view
        # return {
        #     'name': 'Sales Report',
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'res_model': 'butir.sales.report.wizard',
        #     'type': 'ir.actions.act_window',
        #     'res_id': self.id,
        #     'target': 'current',
        # }

        return self.env.ref('bt_ketronics_od12.action_butir_sales_report').report_action(self)
