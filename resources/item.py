import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from models.store import StoreModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help = "This field cannot be left blank!"
        )

    parser.add_argument('store_id',
            type=int,
            required=True,
            help = "Every item needs a store id."
        )
        
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message" : "item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name {} already exist.".format(name)}, 400
        
        #data = request.get_json()
        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        if StoreModel.find_by_id(item.store_id):
            try:
                item.save_to_db()
                return item.json(), 201
            except:
                return {"message" : "An error occured while inserting the item"}, 500   ##internal server error
        else:
            return {"message" : "Store with the given store id does not exists, please provide valid store id."}, 400

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message" : "Item deleted"}
        return {"message" :"NO such item exists to delete."}, 400

    def put(self, name):
        #data  = request.get_json()
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items" : [item.json() for item in ItemModel.query.all()]}
        #return {"item" : list(map(lambda x : x.json(), ItemModel.query.all()))}
