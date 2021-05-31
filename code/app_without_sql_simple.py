from flask import Flask,request
from flask_restful import Resource,Api
from flask_jwt import JWT,jwt_required #json web token for authentication
from security import authenticate,identity
app=Flask(__name__)
app.secret_key="anything"
api=Api(app)

jwt=JWT(app,authenticate,identity)   #it provides  http://127.0.0.1:5000/auth which generates token

items=[]

class Item(Resource):
    @jwt_required()                #now this will return only if it authorized user, #decorate @jwt_required whereevr required
    #steps1: execute POST  http://127.0.0.1:5000/auth with Header "content type - json"  body - raw - {"username":"user1","password":"abcxyz"} --> get access_token
    #step2:GET  http://127.0.0.1:5000/item/chair header : Authorization (KEY) = JWT access_token (Value) of previous (ex: JWT anh12jhj...)
    def get(self,name):
        for item in items:
            if item["name"]==name:
                return {"item":item}
                # always try to use lambda in this case
                #item= next(filter(lambda x: x["name"]==name,items),None) #next provide first item found #return none if no match found
        return {"item":None},404 #if given item not found in list, why 404 , with out 404 HTTP status code will be 200 , so explicitly telling 404 (URL Not fount), chk it is postman with and without 404

    def post(self,name):
        data=request.json
        item={"name":name,"price":data["price"]}
        items.append(item)
        return item,201 #jsonify not required in restful #201 means object created

    def delete(self,name):
        for item in items:
            if item["name"]==name:
                items.remove(item)
                return ({"message":"item deleted"})
        return ({"message":"Item not found"})

    def put(self,name): #add if new obj else update exist
        data=request.json
        item=next(filter(lambda x:x['name']==name,items),None) #None if no match with name
        if item is None: #so here its new obj so add
            item ={"name":name,"price":data["price"]}
            items.append(item)
        else:
            item.update(data) #update if it exist
            #no matters how many times you hit value will never change bcz its just update exist value
        return item


class ItemsList(Resource):
    def get(self):
        return ({"items":items})

api.add_resource(Item,'/item/<string:name>') # nothing but @app.route(//127.0.0.1:5000/some_name) def student()
api.add_resource(ItemsList,'/items')
app.run(debug=True)