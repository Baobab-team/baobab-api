from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from .base import BaseModel
from app.database import Base


class Category(Base):
    __tablename__ = "tbl_categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(), unique=True)
    businesses = relationship("Business", backref="category", lazy=True)

    def __repr__(self):
        return '<Category {}>'.format(self.name)
