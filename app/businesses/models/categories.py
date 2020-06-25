from .base import BaseModel
from app import db


class Category(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    businesses = db.relationship("Business", backref="category", lazy=True)

    def __repr__(self):
        return f'<Category name=f{self.name}, id=f{self.id}>'
