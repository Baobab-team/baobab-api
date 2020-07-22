from datetime import datetime
from enum import Enum

from sqlalchemy_utils import ScalarListType

from app import db
from app.businesses.models.base import TimestampMixin

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('business_id', db.Integer, db.ForeignKey('business.id'), primary_key=True)
                )


class Business(db.Model, TimestampMixin):
    class StatusEnum(Enum):
        pending = "pending"
        accepted = "accepted"
        refused = "refused"

        @staticmethod
        def list():
            return [x.value for x in Business.StatusEnum]

    class PaymentTypeEnum(Enum):
        credit = "credit"
        debit = "debit"
        cash = "cash"
        crypto = "crypto"

        @staticmethod
        def list():
            return [e.value for e in Business.TypeEnum]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String(), nullable=True)
    slogan = db.Column(db.String())
    website = db.Column(db.String(), nullable=True)
    email = db.Column(db.String(), nullable=True, unique=True)
    status = db.Column(db.String(), default=StatusEnum.pending.value)
    accepted_at = db.Column(db.DateTime, nullable=True, default=None)
    notes = db.Column(db.String(), nullable=True)
    capacity = db.Column(db.Integer, nullable=True)
    payment_types = db.Column(ScalarListType(), default=[PaymentTypeEnum.cash.value])
    business_hours = db.relationship('BusinessHour', backref='business', lazy=True)
    addresses = db.relationship('Address', backref='business', lazy=True)
    phones = db.relationship('Phone', backref='business', lazy=True)
    social_links = db.relationship('SocialLink', backref='business', lazy=True)
    tags = db.relationship('Tag', secondary=tags, lazy='subquery',
                           backref=db.backref('businesses', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"), nullable=True)
    business_upload_id = db.Column(db.Integer, db.ForeignKey("business_upload.id"), nullable=True)

    def __eq__(self, other):
        if not isinstance(other, Business):
            return False

        return self.name == other.name and \
               self.description == other.description and \
               self.slogan == other.slogan and \
               self.notes == other.notes and \
               self.website == other.website and \
               self.business_hours == other.business_hours and \
               self.phones == other.phones and \
               self.addresses == other.addresses and \
               self.social_links == other.social_links and \
               self.tags == other.tags

    def __repr__(self):
        key_values = ' , '.join('{}={}'.format(k, v) for (k, v) in self.__dict__.items() if k != '_sa_instance_state')
        return '<{} {}>'.format(type(self).__name__, key_values)

    def process_status(self, status=StatusEnum.pending.value):

        self.status = status

        if status == Business.StatusEnum.accepted.value:
            self.accepted_at = datetime.utcnow()
        else:
            self.accepted_at = None

    def add_business_hour(self, hour):
        self.business_hours.append(hour)

    def add_business_hours(self, hours):
        for hour in hours:
            self.add_business_hour(hour)

    def add_phone(self, phone):
        self.phones.append(phone)

    def add_phones(self, phones):
        for phone in phones:
            self.add_phone(phone)

    def add_address(self, address):
        self.addresses.append(address)

    def add_addresses(self, addresses):
        for address in addresses:
            self.add_address(address)

    def add_social_link(self, social_link):
        self.social_links.append(social_link)

    def add_social_links(self, social_links):
        for social_link in social_links:
            self.add_social_link(social_link)

    def add_tag(self, tag):
        self.tags.append(tag)

    def add_tags(self, tags):
        for tag in tags:
            self.add_tag(tag)


class BusinessUpload(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(), unique=True)
    success = db.Column(db.Boolean(), default=False)
    error_message = db.Column(db.String(), nullable=True)
    businesses = db.relationship('Business', backref='business_upload_log', lazy=True)

    def addBusinesses(self,businesses):
        for b in businesses:
            self.businesses.append(b)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)

    def addBusinessTag(self, business):
        """
        Add item to tags association table
        :param business:
        :return:
        """
        self.businesses.append(business)

    def addBusinessTags(self, businesses):
        for business in businesses:
            self.addBusinessTag(business)

    def removeBusinessTag(self, business):
        index = self.businesses.index(business)
        self.businesses.pop(index)

    def __eq__(self, other):
        if not isinstance(other, Tag):
            return False

        return self.name == other.name

    def __repr__(self):
        key_values = ' , '.join('{}={}'.format(k, v) for (k, v) in self.__dict__.items() if k != '_sa_instance_state')
        return '<{} {}>'.format(type(self).__name__, key_values)

class Address(db.Model):
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
        e = "east"
        n = "north"
        ne = "north east"
        nw = "north west"
        s = "south"
        se = "south east"
        sw = "south West"
        w = "west"
        none = ""

        @staticmethod
        def list():
            return [e.value for e in Address.DirectionEnum]

    id = db.Column(db.Integer, primary_key=True)
    street_number = db.Column(db.String())
    street_type = db.Column(db.String())
    street_name = db.Column(db.String())
    direction = db.Column(db.String())
    city = db.Column(db.String(), default="Montreal")
    zip_code = db.Column(db.String())
    province = db.Column(db.String())
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

    def __eq__(self, other):
        if not isinstance(other, Address):
            return False

        return self.region == other.region and \
               self.country == other.country and \
               self.street_name == other.street_name and \
               self.street_number == other.street_number and \
               self.street_type == other.street_type and \
               self.city == other.city and \
               self.province == other.province and \
               self.country == other.country and \
               self.zip_code == other.zip_code and \
               self.direction == other.direction


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

        @staticmethod
        def list():
            return [e.value for e in BusinessHour.DaysEnum]

    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(), nullable=False)
    closing_time = db.Column(db.Time, nullable=False, default=datetime.utcnow())
    opening_time = db.Column(db.Time, nullable=False, default=datetime.utcnow())
    business_id = db.Column(db.Integer, db.ForeignKey("business.id"))

    def __repr__(self):
        return '<BusinessHour {}: {} to {}>'.format(self.day, self.opening_time, self.closing_time)

    def __eq__(self, other):
        if not isinstance(other, BusinessHour):
            return False

        return self.day == other.day and \
               self.closing_time == other.closing_time and \
               self.opening_time == other.opening_time


class Phone(db.Model):
    """
        Phone model
    """

    class Type(Enum):
        tel = "telephone"
        fax = "fax"

        @staticmethod
        def list():
            return [e.value for e in Phone.Type]

    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String(5), nullable=True)
    number = db.Column(db.String(), nullable=False)
    extension = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), default=Type.tel.value)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'),
                            nullable=False)

    def __eq__(self, other):
        if not isinstance(other, Phone):
            return False

        return self.number == other.number and \
               self.extension == other.extension and \
               self.type == other.type

    def __repr__(self):
        return '<Phone: {}'.format(self.number)


class SocialLink(db.Model):
    class TypeEnum(Enum):
        instragram = "instagram"
        facebook = "facebook"
        linkedin = "linkedin"
        snapchat = "snapchat"
        twitter = "twitter"

        @staticmethod
        def list():
            return [e.value for e in SocialLink.TypeEnum]

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(), nullable=False)
    type = db.Column(db.String())
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)

    def __eq__(self, other):
        if not isinstance(other, SocialLink):
            return False

        return self.link == other.link and \
               self.type == other.type
