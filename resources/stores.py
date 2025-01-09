import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

store_blueprint = Blueprint("stores", __name__, description="Operations on stores")

store_blueprint.route("/stores/<string:store_id>")
class Stores(MethodView):
    def get(self, store_id):
        pass

    def delete(self, store_id):
        pass