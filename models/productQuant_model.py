from odoo import models, fields, api


class ProductQuantModel(models.Model):
    _name = 'bar_app.productq_model'
    _description = ''

    numTable = fields.Many2one(comodel_name="bar_app.table_model",string="Table:")
    product = fields.Many2one(comodel_name="bar_app.product_model",string="Product")
    quant = fields.Integer(string="Quantity:",default=1)
    observations = fields.Char(string="Observations:")
    price = fields.Float(string="Price:",compute="totalPrice", store=True)
    state = fields.Selection(string="Status",selection=[('O','Ordered'),('P','Prepared'),('D','Delivered')], default="O")
    destiny = fields.Selection(string="Destination", selection=[('B',"Bar"),('K','Kitchen')], default="K")

    @api.depends("product.price","quant")
    def totalPrice(self):
        for rec in self:
            rec.price = rec.quant * rec.product.price

    def isPreparedBarman(self):
        self.state = 'P'
        return {
               'name': ('Order List Waiter'),
               'view_type': 'form',
               'view_mode': 'tree,form',
               'res_model': 'bar_app.productq_model',
               'domain': [('state', '=', 'O'),('destiny','=','B')],
               'view_id': False,
               'views':[(self.env.ref('bar_app.productq_model_list_barman').id,'tree'),(self.env.ref('bar_app.productq_model_form_barman').id,'form')],
               'type': 'ir.actions.act_window'
          }

    def isPreparedCook(self):
        self.state = 'P'
        return {
               'name': ('Order List Waiter'),
               'view_type': 'form',
               'view_mode': 'tree,form',
               'res_model': 'bar_app.productq_model',
               'domain': [('state', '=', 'O'),('destiny','=','K')],
               'view_id': False,
               'views':[(self.env.ref('bar_app.productq_model_list_cook').id,'tree'),(self.env.ref('bar_app.productq_model_form_cook').id,'form')],
               'type': 'ir.actions.act_window'
          }

    def isPreparedWaiter(self):
        self.state = 'P'
        return {
               'name': ('Order List Waiter'),
               'view_type': 'form',
               'view_mode': 'tree,form',
               'res_model': 'bar_app.productq_model',
               'domain': [('state', '=', 'P')],
               'view_id': False,
               'views':[(self.env.ref('bar_app.productq_model_list_waiter').id,'tree'),(self.env.ref('bar_app.productq_model_form_waiter').id,'form')],
               'type': 'ir.actions.act_window'
          }

    def isDelivered(self):
        self.state = 'D'
        return {
               'name': ('Order List Waiter'),
               'view_type': 'form',
               'view_mode': 'tree,form',
               'res_model': 'bar_app.productq_model',
               'domain': [('state', '=', 'P')],
               'view_id': False,
               'views':[(self.env.ref('bar_app.productq_model_list_waiter').id,'tree'),(self.env.ref('bar_app.productq_model_form_waiter').id,'form')],
               'type': 'ir.actions.act_window'
          }
