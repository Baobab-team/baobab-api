from datetime import datetime
from enum import Enum

from app import db
from app.common.base import TimestampMixin


class PaymentType(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)


# TODO Change table to plurials
class Category(db.Model):
    """
    Category model
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    businesses = db.relationship("Business", backref="category", lazy=True)

    def __repr__(self):
        return '<Category {}>'.format(self.name)


tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('business_id', db.Integer, db.ForeignKey('business.id'), primary_key=True)
                )


class Business(db.Model, TimestampMixin):
    """
    Business model
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    legal_name = db.Column(db.String(), unique=True, nullable=True)
    description = db.Column(db.String())
    slogan = db.Column(db.String())
    website = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=True)
    accepted_at = db.Column(db.DateTime, nullable=True, default=None)
    notes = db.Column(db.String(), nullable=True)
    capacity = db.Column(db.Integer, nullable=True)

    business_hours = db.relationship('BusinessHour', backref='business', lazy=True)
    address = db.relationship('Address', backref='business', lazy=True)
    phones = db.relationship('Phone', backref='business', lazy=True)
    social_links = db.relationship('SocialLink', backref='business', lazy=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
                           backref=db.backref('pages', lazy=True))
    owner_id = db.Column(db.Integer, db.ForeignKey("owner.id"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    payment_type = db.Column(db.Integer, db.ForeignKey("payment_type.id"), nullable=True)

    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=True)

    def __repr__(self):
        return '<Business {}>'.format(self.name)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)


class Address(db.Model):
    """
    Address for a single business
    """

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
    zip_code = db.Column(db.String())
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
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(), nullable=False)
    extension = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False, default="telephone")
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


class SocialLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)


