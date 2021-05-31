from flask import Flask,jsonify,request,render_template
import json
#jsonify converts dictionary values to json

app=Flask(__name__)

stores=[
    {
        "name":"My Store",
         "items":[
            {
                'name':'My item',
                 'price': 15.99,
                 'ret':None
            }
        ]
    }
]

#Home
@app.route("/")
def home():
    return render_template("index.html")
#POST used to receive the data ans save
#GET used to send data back only

#post /store data: {name :}
@app.route('/store' , methods=['POST'])
def create_store():
  request_data = request.json
  print (request_data)
  new_store = {
    'name':request_data['name'],
    'items':[]
  }
  stores.append(new_store)
  return jsonify(new_store) #its upto programmer what to return whether stores or new_store

# GET /store/<string:name>
@app.route("/store/<string:name>",methods=["GET"]) #http://127.0.0.1:5000/store/some_name
def get_store(name):
    #iterate over stores
    #if the store name matches
    #if none match, return error message
    for store in stores:
        if store["name"]==name:
            return jsonify(store)
        else:
            return jsonify({"Message":"Store not found"})


# GET /store
@app.route("/store",methods=["GET"])
def get_stores():
    #return jsonify(stores) #not works bcz jsonify takes dict values but here stores in list
    return jsonify({'stores':stores})
    #json_string=json.dumps(stores) #if you use json serialaization
    #return ({"stores":json_string})

# POST /store/<string:name>/item
@app.route("/store/<string:name>/item",methods=["POST"])
def create_item_in_store(name):
    request_data=request.json
    for store in stores:
        if store["name"]== name:
            new_item ={
                'name':request_data['name'],
                'price':request_data['price']
            }
            store["items"].append(new_item)
            return jsonify(new_item) ##its upto programmer what to return whether stores or new_item
    return ({"message":"Store not found"})

# GET /store/<string:name>/item
@app.route("/store/<string:name>/item",methods=["GET"])
def get_items_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify(store["items"])
        else:
            return ({"message": "Store not found"})


if __name__ == "__main__":
    app.run(debug=True)