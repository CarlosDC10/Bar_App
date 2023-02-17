from odoo import models, fields, api


class ProductModel(models.Model):
    _name = 'bar_app.product_model'
    _description = 'Model for the products of the menu'

    name = fields.Char(string="Name",help="Name of the products",required=True)
    photo = fields.Binary(string="Photo:",help="Photo of the product")
    description = fields.Text(string="Description",help="Description of the product")
    currency_id = fields.Many2one("res.currency",string="Currency",default=lambda self:self.env.user.company_id.currency_id)
    price = fields.Monetary(string="Price",help="Price of the product",required=True)
    available = fields.Boolean(string="Is available?",help="Is the product available in the menu?",default=True)
    category = fields.Many2many(comodel_name="bar_app.category_model",string="Category",inverse_name="products")
    ingredients = fields.Many2many("bar_app.ingredient_model",string="Ingredients")


    def isAvailable(self):
        self.available = not self.available