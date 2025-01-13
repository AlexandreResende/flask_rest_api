import uuid
import logging

from src.db import db

from sqlalchemy.exc import SQLAlchemyError

from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint

from flask_smorest import Api, abort

from src.schemas import ItemsSchema, ItemUpdateSchema, GetItemsSchema
from src.models import ItemModel

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
        item_data |= { "store_id": uuid.UUID(store_id) }
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            logging.exception("message")
            return { "message": "Failed to persist item" }, 500

        return item.json(), 201

@items_blueprint.route("/stores/<string:store_id>/items/<string:item_id>")
class ItemsWithStore(MethodView):
    @items_blueprint.response(200, ItemsSchema)
    def get(self, store_id, item_id):
        item = ItemModel.query.get(uuid.UUID(item_id))

        if not item:
            return { "message": "Item not found" }, 404
        
        if uuid.UUID(store_id) != item.json()["store_id"]:
            return { "message": "Item does not belong to this store" }, 403
        
        return item, 200
        
    @items_blueprint.arguments(ItemUpdateSchema)
    @items_blueprint.response(200, ItemsSchema)
    def put(self, item_data, store_id, item_id):
        item = ItemModel().query.get(uuid.UUID(item_id))

        if not item:
            return { "message": "Item not found" }, 404
        
        if uuid.UUID(store_id) != item.json()["store_id"]:
            return { "message": "This item does not belong to this store." }, 403

        if "name" in item_data.keys():
            item.name = item_data["name"]
        if "price" in item_data.keys():
            item.price = item_data["price"]

        db.session.add(item)
        db.session.commit()

        return item.json(), 200
        
    def delete(self, store_id, item_id):
        item = ItemModel.query.get(uuid.UUID(item_id))

        if not item:
            return { "message": "Item not found." }, 404

        if uuid.UUID(store_id) != item.json()["store_id"]:
            return { "message": "Item does not belong to store" }, 403

        db.session.delete(item)
        db.session.commit()

        return { "message": "Item deleted" }, 200