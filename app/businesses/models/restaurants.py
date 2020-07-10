from datetime import datetime

from sqlalchemy import Integer, Column, String, Time, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Restaurant(Base):
    __tablename__ = "tbl_restaurants"
    id = Column(Integer, primary_key=True)

    menus = relationship('Menu', backref='tbl_restaurants', lazy=True)


class Menu(Base):
    __tablename__ = "tbl_menus"

    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    start = Column(Time, nullable=False, default=datetime.utcnow())
    end = Column(Time, nullable=True)

    plates = relationship('Plate', backref='tbl_menus', lazy=True)

    restaurant_id = Column(Integer, ForeignKey('tbl_restaurants.id'), nullable=False)


class Plate(Base):
    __tablename__ = "tbl_plates"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(), nullable=False)

    menu_id = Column(Integer, ForeignKey('tbl_menus.id'), nullable=False)

