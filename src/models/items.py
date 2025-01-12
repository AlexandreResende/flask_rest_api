import uuid
import json

from sqlalchemy import *
from sqlalchemy.orm import relationship
from src.db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), unique=False, nullable=False)
    price = Column(Float(precision=2), unique=False, nullable=False)
    store_id = Column(UUID(as_uuid=True), unique=False, nullable=False)
    # store_id = Column(UUID(as_uuid=True), db.ForeignKey("stores.id"), unique=False, nullable=False)
    # store = relationship("StoreModel", back_populates="items")