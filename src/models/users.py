import uuid

from sqlalchemy import *

class UserModel():
  __tablename__ = "users"

  id = Column(UUID(), primary_key=True, default=uuid.uuid4)
  username = Column(String(120), unique=True, nullable=False)
  password = Column(String(120), nullable=False)

  def json(self):
    return {
      "id": self.id,
      "username": self.username,
      "password": self.password
    }