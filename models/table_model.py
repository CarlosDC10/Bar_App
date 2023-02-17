from odoo import models, fields, api, http
from odoo.exceptions import ValidationError
import datetime



class TableModel(models.Model):
    _name = 'bar_app.table_model'
    _description = 'Model for the table of the menu'
    _rec_name="num"

    num = fields.Integer(string="Num: ",help="Number of the table",required=True)
    diners = fields.Integer(string="Diners: ",help="Number of diners in the table")
    client = fields.Char(string="Client:",required=False)
    waiter = fields.Char(string="Waiter:",required=False, default = lambda self: self.env.user.name)
    products = fields.One2many(comodel_name="bar_app.productq_model",inverse_name="numTable",string="Orders:")
    total = fields.Float(string="Total:",compute="getTotal",store=True)
    active=fields.Boolean(string="Is serving",default=True)
    state = fields.Selection(string="Status",selection=[('W','Waiting an order'),('E','Eating order'),('F','Finished')], default="W")
    dateFinished = fields.Datetime(string="Starting date:",default=lambda self: datetime.datetime.now())
    stateOrder = fields.Boolean(string="State of Orders:")

    @api.constrains("diners")
    def checkLenght(self):
        if self.diners<=0:
            raise ValidationError("The num of diners has to be at least 1")

    @api.constrains("num","active")
    def noRepeat(self):
        for a in self:
            for b in self:
                if a.num == b.num and a.id != b.id:
                    if a.active == True:
                        raise ValidationError("The cannot be 2 active tables with the same numbers")
            

    @api.depends("products.state")
    def getTotal(self):
        for record in self:
            record.total=0
            for order in record.products:
                if(order.state == 'D'):
                    record.stateOrder = False
                else:
                    record.stateOrder = True
                    break
            for rec in record.products:
                record.total = record.total + rec.price

    def isActive(self):
        for order in self.products:
                if order.state != 'D':
                    raise ValidationError("There are one or more orders not delivered!!!!")
        self.state = "F"
        self.active = not self.active
        response = {
            "client" : self.client,
            "base":self.total
        }

        invoice = self.env["bar_app.invoice_model"].create(response)
        #products = []
        for prod in self.products:
            product = prod.product
            quant = prod.quant
            price = prod.price
            linea = {
                "invoiceRef": invoice.id,
                "product" : product.id,
                "quant":quant,
                "price": price
            }
            self.env["bar_app.invoiceprod_model"].create(linea)

    def orderGiven(self):
        for order in self.products:
                if order.state != 'D':
                    raise ValidationError("There are one or more orders not delivered!!!!")
        self.state = "E"

    def orderTaken(self):
        self.state = "W"

    @api.depends("state")
    def totalPrice(self):
        for rec in self:
            if rec.state == 'F':
                rec.active = False

    @api.onchange("num")
    def changeNum(self):
        for rec in self:
            rec.client = "Table "+str(rec.num)