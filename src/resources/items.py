import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

from src.db import items, stores
from src.schemas import ItemsSchema, ItemUpdateSchema, GetItemsSchema

items_blueprint = Blueprint("items", __name__, description="Operations on items")
        
@items_blueprint.route("/items")
class Items(MethodView):
    @items_blueprint.response(200, GetItemsSchema)
    def get(self):
        return { "items": list(items.values()) }, 200

@items_blueprint.route("/stores/<string:store_id>/items")
class CreateItem(MethodView):
    @items_blueprint.arguments(ItemsSchema)
    def post(self, item_data, store_id):
        if store_id not in stores:
            return { "message": "Store not found" }, 404
        
        item_id = uuid.uuid4().hex
        items[item_id] = { "id": item_id, "store_id": store_id, **item_data }

        return { **items[item_id] }, 201

@items_blueprint.route("/stores/<string:store_id>/items/<string:item_id>")
class ItemsWithStore(MethodView):
    @items_blueprint.response(200, ItemsSchema)
    def get(self, store_id, item_id):
        try:
            if store_id != items[item_id]["store_id"]:
                return { "message": "Operation not allowed." }, 403
        
            return { **items[item_id] }, 200
        except KeyError:
            return { "message": "Item not found" }, 404 
        
    @items_blueprint.arguments(ItemUpdateSchema)
    @items_blueprint.response(200, ItemsSchema)
    def put(self, item_data, store_id, item_id):
        try:
            item_data = request.get_json()

            item = items[item_id]

            if store_id != item["store_id"]:
                return { "message": "This item does not belong to this store." }, 403

            item |= item_data

            return { **item }, 200

        except KeyError:
            return { "message": "Item not found" }, 404
        
    def delete(self, store_id, item_id):
        try:
            if store_id != items[item_id]["store_id"]:
                return { "message": "Operation not allowed." }, 403

            del items[item_id]

            return {}, 200
        except KeyError:
            return { "message": "Item not found" }, 404