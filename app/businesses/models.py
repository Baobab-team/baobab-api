from datetime import datetime
from enum import Enum

from app import db
from app.common.base import TimestampMixin


class PaymentType(db.Model):
    __tablename__ = 'payment_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)


# TODO Change table to plurials
class Category(db.Model):
    """
    Category model
    """
    __tablename__ = 'category'
    # TODO remove id and use name as primary key
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    businesses = db.relationship("Business", backref="category", lazy=True)

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class Business(db.Model, TimestampMixin):
    """
    Business model
    """
    __tablename__ = 'business'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    legal_name = db.Column(db.String(), unique=True, nullable=True)
    phone = db.Column(db.String())
    description = db.Column(db.String())
    slogan = db.Column(db.String())
    website = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=True)
    accepted = db.Column(db.Boolean, default=False)
    notes = db.Column(db.String(), nullable=True)
    capacity = db.Column(db.Integer, nullable=True)

    business_hours = db.relationship('BusinessHour', backref='business', lazy=True)
    address = db.relationship('Address', backref='business', lazy=True, uselist=False)
    phones = db.relationship('Phone', backref='business', lazy=True, uselist=False)

    owner_id = db.Column(db.Integer, db.ForeignKey("owner.id"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    payment_type = db.Column(db.Integer, db.ForeignKey("payment_type.id"), nullable=True)

    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=True)

    def __repr__(self):
        return '<Business {}>'.format(self.name)


class Address(db.Model):
    """
    Address for a single business
    """
    __tablename__ = 'business_address'

    class ProvinceEnum(Enum):
        qc = "QC"
        on = "ON"
        ns = "NS"
        nb = "NB"
        pe = "PE"
        ab = "AB"
        nu = "NU"
        sk = "SK"
        bc = "BC"
        nl = "NL"
        mb = "MB"

    class DirectionEnum(Enum):
        e = "E"
        n = "N"
        ne = "NE"
        nw = "NW"
        s = "S"
        se = "SE"
        sw = "SW"
        w = "W"

    id = db.Column(db.Integer, primary_key=True)
    street_number = db.Column(db.String())
    street_type = db.Column(db.String(5))
    street_name = db.Column(db.String())
    direction = db.Column(db.String(2))
    city = db.Column(db.String(), default="Montreal")
    province = db.Column(db.String(2))
    region = db.Column(db.String())
    country = db.Column(db.String())
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'),
                            nullable=False)

    def __repr__(self):
        return '<Address {} {} {},{},{}>'.format(self.street_number,
                                                 self.street_name,
                                                 self.street_type,
                                                 self.city,
                                                 self.province)


class BusinessHour(db.Model):
    """
    Business hour  for a single day
    """
    __tablename__ = 'business_hour'

    class DaysEnum(Enum):
        monday = "monday"
        tuesday = "tuesday"
        wednesday = "wednesday"
        thursday = "thursday"
        friday = "friday"
        saturday = "saturday"
        sunday = "sunday"

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(2))
    closing_time = db.Column(db.Time, nullable=False, default=datetime.utcnow())
    opening_time = db.Column(db.Time, nullable=False, default=datetime.utcnow())
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"))

    def __repr__(self):
        return '<BusinessHour {}: {} to {}>'.format(self.day, self.opening_time, self.closing_time)


class Phone(db.Model):
    """
    Phone model
    """
    __tablename__ = "phones"
    number = db.Column(db.String(), primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'),
                            nullable=False)

    def __repr__(self):
        return '<Phone: {}'.format(self.number)


class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    menus = db.relationship('Menu', backref='restaurant', lazy=True)


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    start = db.Column(db.Time, nullable=False, default=datetime.utcnow())
    end = db.Column(db.Time, nullable=True)

    plates = db.relationship('Plate', backref='menu', lazy=True)

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)


class Plate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(), nullable=False)

    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)
