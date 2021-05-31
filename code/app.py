from flask import Flask,request
from flask_restful import Resource, Api
#from flask_jwt import JWT, jwt_required  # json web token for authentication

#from security import authenticate, identity
from items import ItemsList,Item

app=Flask(__name__)
#app.secret_key="anything"
api=Api(app)

#jwt=JWT(app,authenticate,identity)   #it provides  http://127.0.0.1:5000/auth which generates token

items=[]


api.add_resource(Item,'/item/<string:name>') # nothing but @app.route(//127.0.0.1:5000/some_name) def student()
api.add_resource(ItemsList,'/items')

if __name__ == "__main__":
    app.run(debug=True)