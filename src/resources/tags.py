import logging
import uuid
from flask.views import MethodView
from flask_smorest import Blueprint
from src.models.tags import TagModel
from src.models.stores import StoreModel
from src.schemas import TagSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.db import db

tags_blueprint = Blueprint("tags", __name__, description="Operations with tags")

@tags_blueprint.route("/tags")
class Tags(MethodView):
    def get(self):
        tags = TagModel.query.all()
        tags_json = [tag.json() for tag in tags]

        return { "tags": tags_json }, 200

@tags_blueprint.route("/stores/<string:store_id>/tags")
class CreateTag(MethodView):
    @tags_blueprint.arguments(TagSchema)
    def post(self, tag_data, store_id):
        store = StoreModel.query.get(uuid.UUID(store_id))

        if not store:
            return { "message": "Store not found" }, 404

        tag_data |= { "store_id": uuid.UUID(store_id) }
        tag = TagModel(**tag_data)

        try:
            db.session.add(tag)
            db.session.commit()

            return {}, 200
        except IntegrityError:
            logging.exception("message")
            return { "message": "Failed to process operation." }, 403
        except SQLAlchemyError:
            logging.exception("message")
            return { "message": "An internal error occurred." }, 500

@tags_blueprint.route("/stores/<string:store_id>/tags/<string:tag_id>")
class TagsWithId(MethodView):
    def get(self, store_id, tag_id):
        tag = TagModel.query.get(uuid.UUID(tag_id))

        if not tag:
            return { "message": "Tag not found"}, 404

        if tag.store_id != uuid.UUID(store_id):
            return { "message": "Invalid operation" }, 403
        
        return tag.json(), 200

    @tags_blueprint.arguments(TagSchema)
    def put(self, tag_data, store_id, tag_id):
        tag = TagModel.query.get(uuid.UUID(tag_id))

        if not tag:
            return { "message": "Tag not found" }, 404

        if tag.store_id != uuid.UUID(store_id):
            return { "message": "Invalid operation" }, 403
        
        tag.name = tag_data["name"]

        db.session.add(tag)
        db.session.commit()

        return tag.json(), 200

    def delete(self, store_id, tag_id):
        tag = TagModel.query.get(uuid.UUID(tag_id))

        if not tag:
            return { "message": "Tag not found" }, 404

        if uuid.UUID(store_id) != tag.store_id:
            return { "message": "Invalid operation" }, 403
        
        db.session.delete(tag)
        db.session.commit()

        return {}, 200