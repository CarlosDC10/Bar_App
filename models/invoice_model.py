from odoo import models, fields, api
import datetime


class InvoiceModel(models.Model):
    _name = 'bar_app.invoice_model'
    _description = 'Model for the invoices of the bar'
    _rec_name = "ref"

    ref = fields.Integer(string="Reference: ",help="Reference of the invoice", default=lambda self: self.setRef())
    date = fields.Datetime(string="Emitted date: ", default=lambda self: datetime.datetime.now())
    base = fields.Float(string="Total:",compute="getBase",store=True)
    avt = fields.Selection(string="AVT:",selection=[("0",'0%'),("4",'4%'),("10",'10%'),("21","21%")], default="10")
    total = fields.Float(string="Total:",compute="getTotal",store=True)
    products = fields.One2many(comodel_name="bar_app.invoiceprod_model",inverse_name="invoiceRef",string="Lines:")
    client = fields.Char("Client",help="Name of the client",required=True)
    state = fields.Selection(string="State:",selection=[('D','Draft'),('C','Confirmed')], default="D")

    @api.depends("products")
    def getBase(self):
        for record in self:
            record.base=0
            for rec in record.products:
                record.base = record.base + rec.price

    @api.depends("avt","products")
    def getTotal(self):
        for record in self:
            record.total = 0
            record.total = record.total + record.base +(record.base * int(record.avt))/100

    def changeState(self):
        for record in self:
            record.state = 'C'

    def setRef(self):
        result = self.env['bar_app.invoice_model'].search_read()
        if len(result)==0:
            return 1
        else:
            return result[-1]["ref"] +1
