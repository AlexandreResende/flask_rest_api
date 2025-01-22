import uuid
from sqlalchemy import *
from sqlalchemy.orm import relationship
from src.db import db

class TagModel(db.Model):
    __tablename__ = "tags"

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(120), unique=False, nullable=False)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id"), nullable=False)

    store = relationship("StoreModel", back_populates="tags")

    def json(self):
        return { "id": self.id, "name": self.name, "store_id": self.store_id }