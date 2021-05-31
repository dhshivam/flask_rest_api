from flask import Flask
from flask_restful import Resource,Api

app=Flask(__name__)
api=Api(app)

class student(Resource):
    def get(self,name):
        return ({"Student name":name})

api.add_resource(student,'/student/<string:name>') # nothing but @app.route(//127.0.0.1:5000/some_name) def student()
app.run(debug=True)