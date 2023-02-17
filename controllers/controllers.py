from odoo import http
from odoo.http import json,request


class BarApp(http.Controller):
    @http.route(['/bar_app/getProduct','/bar_app/getProduct/<int:prodid>'], auth='public', type="http")
    def getProduct(self,prodid=None, **kw):
        if prodid:
            domain=[("id","=",prodid)]
        else:
            domain=[]
        proddata = http.request.env["bar_app.product_model"].sudo().search_read(domain,["name","available","price","description","category","ingredients"])
        data = {"status":200, "data": proddata}
        return http.Response(json.dumps(data).encode("utf8"),mimetype ="application/json")

    @http.route(['/bar_app/getAllProduct','/bar_app/getAllProduct/<int:prodid>'], auth='public', type="http")
    def getProducts(self,prodid=None, **kw):
        if prodid:
            domain=[("id","=",prodid)]
        else:
            domain=[]
        proddata = http.request.env["bar_app.product_model"].sudo().search_read(domain,["name","price","description","category","ingredients"])
        data = proddata
        return http.Response(json.dumps(data).encode("utf8"),mimetype ="application/json")

    @http.route(['/bar_app/getIngredient','/bar_app/getIngredient/<int:ingreid>'], auth='public', type="http")
    def getIngredient(self,ingreid=None, **kw):
        if ingreid:
            domain=[("id","=",ingreid)]
        else:
            domain=[]
        ingredata = http.request.env["bar_app.ingredient_model"].sudo().search_read(domain,["name","gluten","observations"])
        data = {"status":200, "data": ingredata}
        return http.Response(json.dumps(data).encode("utf8"),mimetype ="application/json")

    @http.route(['/bar_app/getAllIngredient','/bar_app/getAllIngredient/<int:ingreid>'], auth='public', type="http")
    def getIngredients(self,ingreid=None, **kw):
        if ingreid:
            domain=[("id","=",ingreid)]
        else:
            domain=[]
        ingredata = http.request.env["bar_app.ingredient_model"].sudo().search_read(domain,["name","gluten","observations"])
        data = ingredata
        return http.Response(json.dumps(data).encode("utf8"),mimetype ="application/json")

    @http.route(['/bar_app/getAllCategory','/bar_app/getAllCategory/<int:catid>'], auth='public', type="http")
    def getCategories(self,catid=None, recurse=False,**kw):
        if catid:
            domain=[("id","=",catid)]
        else:
            domain=[]
        catdata = http.request.env["bar_app.category_model"].sudo().search_read(domain,["name","description","products","catFather","child_ids"])
        for rec in catdata:
            if rec["catFather"]:
                detdata = self.getCategories(catid=rec["catFather"][0],recurse=True)
                rec["catFather"] = detdata
                if recurse:
                    return rec 
            else:
                if recurse:
                   return catdata
        
        return http.Response(json.dumps(catdata).encode("utf8"),mimetype ="application/json")

    @http.route(['/bar_app/getCategory','/bar_app/getCategory/<int:catid>'], auth='public', type="http")
    def getCategory(self,catid=None, **kw):
        if catid:
            domain=[("id","=",catid)]
        else:
            domain=[]
        catdata = http.request.env["bar_app.category_model"].sudo().search_read(domain,["name","description","products"])
        data = {"status":200, "data": catdata}
        return http.Response(json.dumps(data).encode("utf8"),mimetype ="application/json")

    @http.route(['/bar_app/getTable','/bar_app/getTable/<int:tabid>'], auth='public', type="http")
    def getTable(self,tabid=None, **kw):
        if tabid:
            domain=[("id","=",tabid)]
        else:
            domain=[]
        tabdata = http.request.env["bar_app.table_model"].sudo().search_read(domain,["num","diners","waiter","client","products","total","state"])
        data = {"status":200, "data": tabdata}
        return http.Response(json.dumps(data).encode("utf8"),mimetype ="application/json")

    @http.route(['/bar_app/getAllTable','/bar_app/getAllTable/<int:tabid>'], auth='public', type="http")
    def getTables(self,tabid=None, **kw):
        if tabid:
            domain=[("id","=",tabid)]
        else:
            domain=[]
        tabdata = http.request.env["bar_app.table_model"].sudo().search_read(domain,["num","diners","waiter","client","products","total","state"])
        data =tabdata
        return http.Response(json.dumps(data).encode("utf8"),mimetype ="application/json")

    @http.route(['/bar_app/getOrder','/bar_app/getOrder/<int:orderid>'], auth='public', type="http")
    def getOrder(self,orderid=None, **kw):
        if orderid:
            domain=[("id","=",orderid)]
        else:
            domain=[]
        orderdata = http.request.env["bar_app.productq_model"].sudo().search_read(domain,["product","quant","price","observations"])
        data = {"status":200, "data": orderdata}
        return http.Response(json.dumps(data).encode("utf8"),mimetype ="application/json")

    @http.route(['/bar_app/getAllOrder','/bar_app/getAllOrder/<int:orderid>'], auth='public', type="http")
    def getOrders(self,orderid=None, **kw):
        if orderid:
            domain=[("id","=",orderid)]
        else:
            domain=[]
        orderdata = http.request.env["bar_app.productq_model"].sudo().search_read(domain,["numTable","product","quant","price","observations","state"])
        orders = []
        for order in orderdata:
            if order["state"] == 'P' or order["state"] == 'O':
                orders.append(order)
        data = orders
        return http.Response(json.dumps(data).encode("utf8"),mimetype ="application/json")

    @http.route(['/bar_app/getInvoice','/bar_app/getInvoice/<int:invid>'], auth='public', type="http")
    def getInvoice(self,invid=None, **kw):
        if invid:
            domain=[("id","=",invid)]
        else:
            domain=[]
        invdata = http.request.env["bar_app.invoice_model"].sudo().search_read(domain,["ref","date","base","avt","total","products","client","state"])
        for rec in invdata:
            rec["date"] = rec["date"].isoformat()
        data = {"status":200, "data": invdata}
        return http.Response(json.dumps(data).encode("utf8"),mimetype ="application/json")

    @http.route(['/bar_app/getInvLine','/bar_app/getInvLine/<int:lineid>'], auth='public', type="http")
    def getInvLine(self,lineid=None, **kw):
        if lineid:
            domain=[("id","=",lineid)]
        else:
            domain=[]
        linedata = http.request.env["bar_app.invoiceprod_model"].sudo().search_read(domain,["product","quant","price"])
        data = {"status":200, "data": linedata}
        return http.Response(json.dumps(data).encode("utf8"),mimetype ="application/json")

    @http.route('/bar_app/addProduct', auth='public', type="json",method="POST")
    def addProduct(self, **kw):
        response = request.jsonrequest
        try:
            result= http.request.env["bar_app.product_model"].sudo().create(response)
            data={
                "status":201,
                "id":result.id
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data

    @http.route('/bar_app/addCategory', auth='public', type="json",method="POST")
    def addCategory(self, **kw):
        response = request.jsonrequest
        try:
            result= http.request.env["bar_app.category_model"].sudo().create(response)
            data={
                "status":201,
                "id":result.id
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data

    @http.route('/bar_app/addIngredient', auth='public', type="json",method="POST")
    def addIngredient(self, **kw):
        response = request.jsonrequest
        try:
            result= http.request.env["bar_app.ingredient_model"].sudo().create(response)
            data={
                "status":201,
                "id":result.id
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data

    @http.route('/bar_app/addTable', auth='public', type="json",method="POST")
    def addTable(self, **kw):
        response = request.jsonrequest
        try:
            result= http.request.env["bar_app.table_model"].sudo().create(response)
            data={
                "status":201,
                "id":result.id
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data

    @http.route('/bar_app/addOrder', auth='public', type="json",method="POST")
    def addOrder(self, **kw):
        response = request.jsonrequest
        try:
            result= http.request.env["bar_app.productq_model"].sudo().create(response)
            data={
                "status":201,
                "id":result.id
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data

    @http.route('/bar_app/updateProduct', auth='public', type="json",method="PUT")
    def updateProduct(self, **kw):
        response = request.jsonrequest
        try:
            proddata = http.request.env["bar_app.product_model"].sudo().search([("id","=",response["id"])])
            proddata.sudo().write(response)
            data={
                "status":201,
                "id":proddata.id
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data

    @http.route('/bar_app/updateCategory', auth='public', type="json",method="PUT")
    def updateCategory(self, **kw):
        response = request.jsonrequest
        try:
            catdata = http.request.env["bar_app.category_model"].sudo().search([("id","=",response["id"])])
            catdata.sudo().write(response)
            data={
                "status":201,
                "id":catdata.id
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data

    @http.route('/bar_app/updateIngredient', auth='public', type="json",method="PUT")
    def updateIngredient(self, **kw):
        response = request.jsonrequest
        try:
            ingredata = http.request.env["bar_app.ingredient_model"].sudo().search([("id","=",response["id"])])
            ingredata.sudo().write(response)
            data={
                "status":201,
                "id":ingredata.id
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data

    @http.route('/bar_app/updateTable', auth='public', type="json",method="PUT")
    def updateTable(self, **kw):
        response = request.jsonrequest
        try:
            tabledata = http.request.env["bar_app.table_model"].sudo().search([("id","=",response["id"])])
            tabledata.sudo().write(response)
            data={
                "status":201,
                "id":tabledata.id
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data

    @http.route('/bar_app/updateOrder', auth='public', type="json",method="PUT")
    def updateOrder(self, **kw):
        response = request.jsonrequest
        try:
            orderdata = http.request.env["bar_app.productq_model"].sudo().search([("id","=",response["id"])])
            orderdata.sudo().write(response)
            data={
                "status":201,
                "id":orderdata.id
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data

    @http.route('/bar_app/deleteProduct', auth='public', type="json",method="DELETE")
    def deleteProduct(self, **kw):
        response = request.jsonrequest
        try:
            proddata = http.request.env["bar_app.product_model"].sudo().search([("id","=",response["id"])])
            proddata.sudo().unlink()
            data={
                "status":200,
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data

    @http.route('/bar_app/deleteCategory', auth='public', type="json",method="DELETE")
    def deleteCategory(self, **kw):
        response = request.jsonrequest
        try:
            catdata = http.request.env["bar_app.category_model"].sudo().search([("id","=",response["id"])])
            catdata.sudo().unlink()
            data={
                "status":200,
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data

    @http.route('/bar_app/deleteIngredient', auth='public', type="json",method="DELETE")
    def deleteIngredient(self, **kw):
        response = request.jsonrequest
        try:
            ingredata = http.request.env["bar_app.ingredient_model"].sudo().search([("id","=",response["id"])])
            ingredata.sudo().unlink()
            data={
                "status":200,
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data

    @http.route('/bar_app/deleteTable', auth='public', type="json",method="DELETE")
    def deleteTable(self, **kw):
        response = request.jsonrequest
        try:
            tabledata = http.request.env["bar_app.table_model"].sudo().search([("id","=",response["id"])])
            tabledata.sudo().unlink()
            data={
                "status":200,
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data

    @http.route('/bar_app/deleteOrder', auth='public', type="json",method="DELETE")
    def deleteOrder(self, **kw):
        response = request.jsonrequest
        try:
            orderdata = http.request.env["bar_app.productq_model"].sudo().search([("id","=",response["id"])])
            orderdata.sudo().unlink()
            data={
                "status":200,
            }
            return data
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data

    @http.route('/bar_app/endTable', auth='public', type="json",method="PUT")
    def endTable(self, **kw):
        response = request.jsonrequest
        try:
            tabledata = http.request.env["bar_app.table_model"].sudo().search([("id","=",response["id"])])
            tabledata.isActive()
            return {
                "status" : 200
            }
        except Exception as e:
            data={
                "status":404,
                "error":e
            }
            return data