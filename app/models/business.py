# Define a base model for other database tables to inherit
from enum import Enum
from datetime import datetime

from sqlalchemy_utils import ChoiceType

from app import db
from app.models.base import Base, TimestampMixin


class Category(Base):
    """
    Category model
    """
    __tablename__ = 'category'

    name = db.Column(db.String(), unique=True)
    businesses = db.relationship("Business", backref="category", lazy=True)

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class StreetTypeEnum(Enum):
    st = "ST"
    ave = "AVE"
    blvd = "BLVD"
    ch = "CH"


class Business(TimestampMixin, Base):
    """
    Business model
    """
    __tablename__ = 'business'

    name = db.Column(db.String(), unique=True, nullable=False)
    phone = db.Column(db.String())
    description = db.Column(db.String())
    website = db.Column(db.String(), nullable=True)
    telephone = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=True)
    accepted = db.Column(db.Boolean, default=False)
    notes = db.Column(db.String(), nullable=True)

    ratings = db.relationship('Rating', backref='business', lazy=True)
    business_hours = db.relationship('BusinessHour', backref='business', lazy=True)
    address = db.relationship('Address', backref='business', lazy=True, uselist=False)

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

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
    street_type = db.Column( db.String(5))
    street_name = db.Column(db.String())
    direction = db.Column(db.String(2))
    city = db.Column(db.String(), default="Montreal")
    province = db.Column(db.String(2))
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'),
                            nullable=False)

    def __repr__(self):
        return '<Address {} {} {},{},{}>'.format(self.street_number, self.street_name, self.street_type, self.city,
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
    closing_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    opening_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"))

    def __repr__(self):
        return '<BusinessHour {}: {} to {}>'.format(self.day, self.opening_time, self.closing_time)


class FavoriteBusiness(Base):
    """
    User's favorite business
    """
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    favorite = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<FavoriteBusiness business={}, user={}>'.format(self.business_id, self.user_id)


class Rating(TimestampMixin, Base):
    """
    Rating for business
    """
    __tablename__ = 'rating'

    business_id = db.Column(db.Integer, db.ForeignKey("business.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    comment = db.Column(db.String(), nullable=True)
    rate = db.Column(db.Integer)

    def __repr__(self):
        return '<Rating {} {}>'.format(self.rate, self.comment)
