from datetime import datetime
from enum import Enum

from sqlalchemy_utils import ChoiceType

from app import db
from app.common.base import TimestampMixin


class PaymentType(db.Model):
    class TypeEnum(Enum):
        credit = "credit"
        debit = "debit"
        cash = "cash"
        crypto = "crypto"

        @staticmethod
        def list():
            return [e.value for e in PaymentType.TypeEnum]

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(ChoiceType(TypeEnum, impl=db.String()), default="cash")



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

payment_types = db.Table('payment_types',
                         db.Column('payment_type_id', db.Integer, db.ForeignKey('payment_type.id'), primary_key=True),
                         db.Column('business_id', db.Integer, db.ForeignKey('business.id'), primary_key=True)
                         )


class Business(db.Model, TimestampMixin):
    """
    Business model
    """

    class StatusEnum(Enum):
        pending = "pending"
        accepted = "accepted"
        refused = "refused"

        @staticmethod
        def list():
            return [x.value for x in Business.StatusEnum]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String())
    slogan = db.Column(db.String())
    website = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=True)
    status = db.Column(ChoiceType(StatusEnum, impl=db.String()), default="pending")
    accepted_at = db.Column(db.DateTime, nullable=True, default=None)
    notes = db.Column(db.String(), nullable=True)
    capacity = db.Column(db.Integer, nullable=True)

    business_hours = db.relationship('BusinessHour', backref='business', lazy=True)
    addresses = db.relationship('Address', backref='business', lazy=True)
    phones = db.relationship('Phone', backref='business', lazy=True)
    social_links = db.relationship('SocialLink', backref='business', lazy=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
                           backref=db.backref('pages', lazy=True))
    payment_types = db.relationship('PaymentType', secondary=payment_types, lazy='subquery',
                                    backref=db.backref('payment_types', lazy=True))
    owner_id = db.Column(db.Integer, db.ForeignKey("owner.id"), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=True)

    def __repr__(self):
        return '<Business {}>'.format(self.name)

    def process_status(self, status=StatusEnum.pending.value):

        self.status = status

        if status == Business.StatusEnum.accepted.value:
            self.accepted_at = datetime.utcnow()
        else:
            self.accepted_at = None



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

        @staticmethod
        def list():
            return [e.value for e in Address.ProvinceEnum]

    class DirectionEnum(Enum):
        e = "East"
        n = "North"
        ne = "North East"
        nw = "North West"
        s = "South"
        se = "South East"
        sw = "South West"
        w = "West"
        none = ""

        @staticmethod
        def list():
            return [e.value for e in Address.DirectionEnum]

    id = db.Column(db.Integer, primary_key=True)
    street_number = db.Column(db.String())
    street_type = db.Column(db.String(5))
    street_name = db.Column(db.String())
    direction = db.Column(ChoiceType(DirectionEnum, impl=db.String()))
    city = db.Column(db.String(), default="Montreal")
    zip_code = db.Column(db.String())
    province = db.Column(ChoiceType(ProvinceEnum, impl=db.String()))
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
    day = db.Column(ChoiceType(DaysEnum, impl=db.String()))
    closing_time = db.Column(db.Time, nullable=False, default=datetime.utcnow())
    opening_time = db.Column(db.Time, nullable=False, default=datetime.utcnow())
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"))

    def __repr__(self):
        return '<BusinessHour {}: {} to {}>'.format(self.day, self.opening_time, self.closing_time)


class Phone(db.Model):
    """
        Phone model
    """

    class Type(Enum):
        tel = "telephone"
        fax = "fax"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(), nullable=False)
    extension = db.Column(db.String(), nullable=False)
    type = db.Column(ChoiceType(Type, impl=db.String()))
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
    class TypeEnum(Enum):
        instragram = "Instagram"
        facebook = "Facebook"
        linkedin = "LinkedIn"
        snapchat = "Snapchat"
        twitter = "Twitter"

        @staticmethod
        def list():
            return [e.value for e in SocialLink.TypeEnum]

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(), nullable=False)
    type = db.Column(ChoiceType(TypeEnum, impl=db.String()))
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)


