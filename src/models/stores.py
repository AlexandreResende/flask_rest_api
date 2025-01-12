import uuid

from sqlalchemy import *
from sqlalchemy.orm import relationship
from src.db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), unique=True, nullable=False)
    # items = relationship("ItemModel", back_populates="store", lazy="dynamic")

    def json(self):
        return { "id": self.id, "name": self.name }