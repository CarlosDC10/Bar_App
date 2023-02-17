from odoo import models, fields, api


class InvoiceProdModel(models.Model):
    _name = 'bar_app.invoiceprod_model'
    _description = ''

    invoiceRef = fields.Many2one(comodel_name="bar_app.invoice_model",string="Invoice Reference:")
    product = fields.Many2one(comodel_name="bar_app.product_model",string="Product")
    quant = fields.Integer(string="Quantity:",default=1)
    price = fields.Float(string="Price:",compute="totalPrice", store=True)

    @api.depends("product.price","quant")
    def totalPrice(self):
        for rec in self:
            rec.price = rec.quant * rec.product.price