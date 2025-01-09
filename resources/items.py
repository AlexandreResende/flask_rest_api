import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from db import items, stores

items_blueprint = Blueprint("items", __name__, description="Operations on items")
        
@items_blueprint.route("/items")
class Items(MethodView):
    def get(self):
        return { "items": list(items.values()) }, 200

@items_blueprint.route("/stores/<string:store_id>/items")
class CreateItem(MethodView):
    def post(self, store_id):
        item_data = request.get_json()

        if store_id not in stores:
            return { "message": "Store not found" }, 404
        
        if (
            "name" not in item_data and not isinstance(item_data["name"], str)
            or "price" not in item_data and not isinstance(item_data["price"], float)
        ):
            return { "message": "Ensure name and price are in the payload with its corresponding types."}, 400
        
        item_id = uuid.uuid4().hex
        items[item_id] = { "id": item_id, "store_id": store_id, **item_data }

        return { **items[item_id] }, 201

@items_blueprint.route("/stores/<string:store_id>/items/<string:item_id>")
class ItemsWithStore(MethodView):
    def get(self, store_id, item_id):
        if store_id != items[item_id]["store_id"]:
                return { "message": "Operation not allowed." }, 403
        
        try:
            return { **items[item_id] }, 200
        except KeyError:
            return { "message": "Item not found" }, 404 
        
    def put(self, store_id, item_id):
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