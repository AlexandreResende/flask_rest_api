import uuid
from flask import Flask, request
from db import items, stores
from flask_smorest import Api, abort

from resources.stores import stores_blueprint as StoresBlueprint
from resources.items import items_blueprint as ItemsBlueprint

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = ""
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist"

api = Api(app)

api.register_blueprint(ItemsBlueprint)
api.register_blueprint(StoresBlueprint)
