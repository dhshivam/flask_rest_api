from flask import Flask,request
#from flask_jwt import JWT, jwt_required  # json web token for authentication
#from security import authenticate, identity
from flask_restful import Resource, Api
import sqlite3
import json

items=[]
class Item(Resource):


    @classmethod
    def find_by_name(cls,name):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        query = "SELECT * from items where name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        db.close()

        if row:
            return {"item": {'name': row[0], 'price': row[1]}}
    #@jwt_required()                #now this will return only if it authorized user, #decorate @jwt_required whereevr required
    #steps1: execute POST  http://127.0.0.1:5000/auth with Header "content type - json"  body - raw - {"username":"user1","password":"abcxyz"} --> get access_token
    #step2:GET  http://127.0.0.1:5000/item/chair header : Authorization (KEY) = JWT access_token (Value) of previous (ex: JWT anh12jhj...)
    def get(self,name):
        '''
        for item in items:
            if item["name"]==name:
                return {"item":item}
                # always try to use lambda in this case
                #item= next(filter(lambda x: x["name"]==name,items),None) #next provide first item found #return none if no match found
        return {"item":None},404 #if given item not found in list, why 404 , with out 404 HTTP status code will be 200 , so explicitly telling 404 (URL Not fount), chk it is postman with and without 404
        '''
        item=self.find_by_name(name)
        if item:
            return item
        return {"Message":"Not found"}


    def post(self,name):
        if self.find_by_name(name):
            return {"Message":"An item with name {} already exist".format(name)}
        data=request.json

        item={"name":name,"price":data["price"]}

        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        query="INSERT INTO items values (?,?)"
        cursor.execute(query,(item['name'],item['price']))

        db.commit()
        db.close()

        return item,201 #jsonify not required in restful #201 means object created

    def delete(self,name):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        cursor.execute("select name from items")

        query = "DELETE FROM items where name=?"
        cursor.execute(query, (name,))

        db.commit()
        db.close()

        return ({"Message":"Item deleted"})
    def put(self,name): #add if new obj else update exist
        '''
        data=request.json
        item=next(filter(lambda x:x['name']==name,items),None) #None if no match with name
        if item is None: #so here its new obj so add
            item ={"name":name,"price":data["price"]}
            items.append(item)
        else:
            item.update(data) #update if it exist
            #no matters how many times you hit value will never change bcz its just update exist value
        return item
        '''
        data=request.json
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        query = "select * from items"
        cursor.execute(query)
        result=cursor.fetchall()
        for i in result:
            if name == i[0]:
                query1="UPDATE items SET name=?"
                cursor.execute(query1,(name,))
                return ({"Message":"Item updated"})
            else:
                item={"name":name,"price":data["price"]}
                query = "INSERT INTO items values (?,?)"
                cursor.execute(query, (item['name'], item['price']))
                return {"Message":"Item inserted"}


class ItemsList(Resource):
    def get(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        query = "select * from items"
        cursor.execute(query)
        items=cursor.fetchall()
        return {"items":items}
