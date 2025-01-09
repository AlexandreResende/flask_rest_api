import uuid
from flask import Flask, request
from db import items, stores
from flask_smorest import Api, abort

from resources.stores import stores_blueprint as StoresBlueprint
from resources.items import items_blueprint as ItemsBlueprint

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["APP_TITLE"] = ""
app.config["VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist"

api = Api(app)

api.register_blueprint(ItemsBlueprint)
api.register_blueprint(StoresBlueprint)


@app.post("/stores/<string:store_id>/items")
def create_store_item(store_id):
    item_data = request.get_json()

    if (
        "price" not in item_data or
        "name" not in item_data
    ):
        abort(400, message="Ensure price and name are included in the payload.")

    if store_id not in stores:
        abort(404, message="Store not found.")
    
    for item in items.values():
        if (
            item["name"] ==  item_data["name"] and
            item["store_id"] == item_data["store_id"]
        ):
            abort(403, "Item already exists.")

    item_data = request.get_json()
    item_id = uuid.uuid4().hex

    items[item_id] = { "store_id": store_id, **item_data }

    return { "id": item_id, "store_id": store_id, **item_data }, 201




# start using variables on postman