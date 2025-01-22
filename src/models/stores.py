import uuid

from sqlalchemy import *
from sqlalchemy.orm import relationship
from src.db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), unique=True, nullable=False)
    items = relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    tags = relationship("TagModel", back_populates="store", lazy="dynamic")

    def json(self):
        return { "id": self.id, "name": self.name, "items": [item.json() for item in self.items], "tags": [tag.json() for tag in self.tags] }