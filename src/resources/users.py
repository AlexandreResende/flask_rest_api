import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from src.schemas import UserSchema
from src.models import UserModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from src.db import db
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

users_blueprint = Blueprint("users", __name__, description="Operation on users")

@users_blueprint.route("/users")
class Users(MethodView):
  @users_blueprint.arguments(UserSchema)
  def post(self, user_data):
    user = UserModel(
      username = user_data["username"],
      password = pbkdf2_sha256.hash(user_data["password"])
    )

    try:
      db.session.add(user)
      db.session.commit()

      return {}, 201
    except IntegrityError:
      return { "message": "An internal error occurred" }, 500
    except SQLAlchemyError:
      return { "message": "An internal error occurred" }, 500

@users_blueprint.route("/users/<string:user_id>")
class OperationOnUsers(MethodView):
  def get(self, user_id):
    user = UserModel.query.get(uuid.UUID(user_id))

    if not user:
      return {}, 404
    
    return user.json(), 200

  def delete(self, user_id):
    user = UserModel.query.get(uuid.UUID(user_id))

    if not user:
      return {}, 404
    
    db.session.delete(user)
    db.session.commit()

    return {}, 200

@users_blueprint.route("/users/login")
class UsersLogin(MethodView):
  @users_blueprint.arguments(UserSchema)
  def post(self, user_data):
    user = UserModel.query.filter(
      UserModel.username == user_data["username"],
    ).first()

    if not user:
      return {}, 404
    
    if pbkdf2_sha256.verify(user_data["password"], user.password):
      access_token = create_access_token(identity=user.id)

      return { "access_token": access_token }, 200
    
    return {}, 401
