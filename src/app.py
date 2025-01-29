import os
from flask import Flask
from flask_jwt_extended import JWTManager

from src.db import db

from src.resources.stores import stores_blueprint as StoresBlueprint
from src.resources.items import items_blueprint as ItemsBlueprint
from src.resources.tags import tags_blueprint as TagsBlueprint
from src.resources.users import users_blueprint as UsersBlueprint

def create_app(db_url=None):

    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = ""
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    app.config["JWT_SECRET_KEY"] = "some_secret_key_here"
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(ItemsBlueprint)
    app.register_blueprint(StoresBlueprint)
    app.register_blueprint(TagsBlueprint)
    app.register_blueprint(UsersBlueprint)

    return app