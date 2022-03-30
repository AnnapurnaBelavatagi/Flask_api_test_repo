from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT
from pip import main

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "Annu"
api = Api(app)

jwt = JWT(app, authenticate,identity)  #/auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)


##this is my first commmit



'''
##Resouce are usually mapped to the db table

app = Flask(__name__)

api = Api(app)

### in restful Api each call is a resource 
class Student(Resource):
    def get(self, name):
        print(name)
        return {'student' : name}

###creating/addinf Student Resource  no decorator is needed 
api.add_resource(Student, '/student/<string:name>') 

app.run(port=5000)

'''

'''
app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    def get(self, name):
        for item in items:
            if item["name"] == name:
                return item
        return {"item" : None}, 404
        

    def post(self, name):
        item = {"name" : name, "price": 12.09}
        items.append(item)
        return item, 201

api.add_resource(Item, "/item/<string:name>")

app.run(port=5000)

'''

'''
app = Flask(__name__)
app.secret_key = "Annu"
api = Api(app)

jwt = JWT(app, authenticate,identity)  #/auth

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help = "This field cannot be left blank!"
        )
        
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item" : item}, 200 if item is not None else item
        
    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"message": "An item with name {} already exist.".format(name)}, 400
        
        #data = request.get_json()
        data = Item.parser.parse_args()

        item = {"name" : name, "price": data["price"]}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name']!= name, items))
        return {"message" : "Item deleted"}
        
    def put(self, name):

        #data  = request.get_json()
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name' :name, 'price' :data['price']}
            items.append(item)
        else:
            item.update(data)

        return item


class ItemList(Resource):
    def get(self):
        return {"items" : items}

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")


app.run(port=5000, debug=True)

'''

