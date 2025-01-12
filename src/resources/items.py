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

        return item_data, 201

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