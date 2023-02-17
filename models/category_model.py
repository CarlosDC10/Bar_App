from odoo import models, fields, api


class CategoryModel(models.Model):
    _name = 'bar_app.category_model'
    _description = 'Model for the categories of the menu'
    _rec_name= 'complete_name'
    _order = 'complete_name'

    name = fields.Char(string="Name: ",help="Name of the category(Salads,openings...)")
    complete_name = fields.Char("Complete name",compute="compute_complete_name",recursive=True,store=True)
    description = fields.Text(string="Description: ",help="Description of the category")
    products = fields.Many2many(comodel_name="bar_app.product_model",inverse_name="category")
    catFather =  fields.Many2one("bar_app.category_model",string="Parent Category",index=True,ondelete="cascade")
    child_ids = fields.One2many("bar_app.category_model","catFather",string="Child categories")

    @api.depends("name","catFather.complete_name")
    def compute_complete_name(self):
        for category in self:
            if category.catFather:
                category.complete_name = '%s/%s' % (category.catFather.complete_name,category.name)
            else:
                category.complete_name = category.name
