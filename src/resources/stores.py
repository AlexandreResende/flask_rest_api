import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from src.schemas import StoreSchema
from src.models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.db import db

stores_blueprint = Blueprint("stores", __name__, description="Operations on stores")

@stores_blueprint.route("/stores")
class Stores(MethodView):
    def get(self):
        return { "stores": list(stores.values()) }, 200
    
    @stores_blueprint.arguments(StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            return { "message": "Store already exists" }, 403
        except SQLAlchemyError:
            return { "message": "An error occurred when persisting a store" }, 500
        return store_data, 201


@stores_blueprint.route("/stores/<string:store_id>")
class StoresWithId(MethodView):
    def get(self, store_id):
        try:
            return { **stores[store_id] }, 200
        except KeyError:
            return { "message": "Store not found." }, 404
        
    def put(self, store_id):
        try:
            store_data = request.get_json()

            stores[store_id] |= store_data

            return {}, 200
        except KeyError:
            return { "message": "Store not found." }, 404 

    def delete(self, store_id):
        try:
            return {}, 200
        except KeyError:
            return { "message": "Store not found." }, 404