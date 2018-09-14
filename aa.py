from flask import Flask
from flask_pymongo import PyMongo
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

from bson import json_util, ObjectId
import json
import requests

app = Flask(__name__)
api = Api(app)
app.config["MONGO_DBNAME"] = 'kindestproject'
app.config["MONGO_URI"] = "mongodb://aa:000000a@ds255768.mlab.com:55768/kindestproject"
mongo = PyMongo(app)
CORS(app)

class Advertisement(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('senderId', type=str)
        args = parser.parse_args()
        if args["senderId"]:
            return json.loads(json_util.dumps(mongo.db.Advertisement.find({"senderId": args["senderId"]})))
        else:
            return json.loads(json_util.dumps(mongo.db.Advertisement.find()))

class Business(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('Name', type=str)
        args = parser.parse_args()
        if args["Name"]:
             return json.loads(json_util.dumps(mongo.db.Business.find({"Name": args["Name"]})))
        else:
            return json.loads(json_util.dumps(mongo.db.Business.find()))


class Geofence(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('latlong', type=str)
        args = parser.parse_args()
        payload = {'layer_ids': '123', 'key_attribute': 'NAME','app_id':'GtJB1ZeogfmrKE9MtF0q','app_code':'Jo501wk-xwsDDwH37_10tQ','proximity':args['latlong']}
        r = requests.get('https://gfe.api.here.com/2/search/proximity.json',params=payload)
        x= r.json()
        a= x['geometries']
        if not a:
            return ("You are not in this area!")
        else:
            b= x['geometries'][0]['attributes']['NAME']
            return b

class User(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=int)
        parser.add_argument('pin', type=int)
        args = parser.parse_args()
      
        if args["username"] :   
            return json.loads(json_util.dumps(mongo.db.User.find({"username": args["username"]})))
        else:
            return ("Please log in again!!!")

api.add_resource(Advertisement, '/ads')
api.add_resource(Business, '/business')
api.add_resource(Geofence, '/geofence')
api.add_resource(User, '/user')
        

if __name__ == '__main__'  :
    app.run(debug=True)