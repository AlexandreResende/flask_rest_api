import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from src.schemas import StoreSchema, StoreUpdateSchema
from src.models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.db import db

stores_blueprint = Blueprint("stores", __name__, description="Operations on stores")

@stores_blueprint.route("/stores")
class Stores(MethodView):
    def get(self):
        stores = StoreModel.query.all()
        store_json = [store.json() for store in stores]
        return { "stores": store_json }, 200
    
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
        return store.json(), 201


@stores_blueprint.route("/stores/<string:store_id>")
class StoresWithId(MethodView):
    def get(self, store_id):
        store = StoreModel.query.get(uuid.UUID(store_id))

        if not store:
            return { "message": "Store not found" }, 404
        
        return store.json(), 200
        
    @stores_blueprint.arguments(StoreUpdateSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get(uuid.UUID(store_id))

        if not store:
            return { "message": "Store not found." }, 404 
        
        store.name = store_data["name"]

        db.session.add(store)
        db.session.commit()

        return store.json(), 200

    def delete(self, store_id):
        store = StoreModel.query.get(uuid.UUID(store_id))

        if not store:
            return { "message": "Store not found." }, 404

        db.session.delete(store)
        db.session.commit()
        
        return {}, 200