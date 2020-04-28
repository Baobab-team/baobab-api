from datetime import datetime

from .base import BaseModel
from app import db


class Restaurant(BaseModel):
    id = db.Column(db.Integer, primary_key=True)

    menus = db.relationship('Menu', backref='restaurant', lazy=True)


class Menu(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    start = db.Column(db.Time, nullable=False, default=datetime.utcnow())
    end = db.Column(db.Time, nullable=True)

    plates = db.relationship('Plate', backref='menu', lazy=True)

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)


class Plate(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(), nullable=False)

    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)

