from odoo import models, fields, api


class IngredientModel(models.Model):
    _name = 'bar_app.ingredient_model'
    _description = 'Model for the ongedients of the products'

    name = fields.Char(string="Name: ",help="Name of the ingredient",required=True)
    gluten = fields.Boolean(string="Gluten free:",help="Is the ingredient gluten free?")
    observations = fields.Html(string="Observations:", help="Num of kcal, fats, protein...")
    products = fields.Many2many("bar_app.product_model", string="Products")

    def glutenFree(self):
        self.gluten = not self.gluten
