from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, ForeignKey, String, Table, DateTime, Boolean, Time
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import ScalarListType

from app.businesses.models.base import TimestampMixin
from app.database import Base

tags = Table('tbl_business_tags',Base.metadata,
                Column('tag_id', Integer, ForeignKey('tbl_tags.id')),
                Column('business_id', Integer, ForeignKey('tbl_businesses.id'))
                )


class Business(Base, TimestampMixin):
    __tablename__ = "tbl_businesses"

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

    id = Column(Integer, primary_key=True)
    name = Column(String(), unique=True, nullable=False)
    description = Column(String(), nullable=True)
    slogan = Column(String())
    website = Column(String(), nullable=True)
    email = Column(String(), nullable=True, unique=True)
    status = Column(String(), default=StatusEnum.pending.value)
    accepted_at = Column(DateTime, nullable=True, default=None)
    notes = Column(String(), nullable=True)
    capacity = Column(Integer, nullable=True)
    payment_types = Column(ScalarListType(), default=[PaymentTypeEnum.cash.value])
    business_hours = relationship('BusinessHour', backref='tbl_businesses', lazy=True)
    addresses = relationship('Address', backref='tbl_businesses', lazy=True)
    phones = relationship('Phone', backref='tbl_businesses', lazy=True)
    social_links = relationship('SocialLink', backref='tbl_businesses', lazy=True)
    tags = relationship('Tag', secondary=tags, lazy='subquery',
                           backref=backref('tbl_businesses', lazy=True))

    category_id = Column(Integer, ForeignKey("tbl_categories.id"), nullable=False)

    restaurant_id = Column(Integer, ForeignKey("tbl_restaurants.id"), nullable=True)
    business_upload_id = Column(Integer, ForeignKey("tbl_business_uploads.id"), nullable=True)

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


class BusinessUpload(Base, TimestampMixin):
    __tablename__ = "tbl_business_uploads"

    id = Column(Integer, primary_key=True)
    filename = Column(String(), unique=True)
    success = Column(Boolean(), default=False)
    error_message = Column(String(), nullable=True)
    businesses = relationship('Business', backref='tbl_business_uploads', lazy=True)

    def addBusinesses(self, businesses):
        for b in businesses:
            self.businesses.append(b)


class Tag(Base):
    __tablename__ = "tbl_tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(), unique=True)

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

class Address(Base):
    __tablename__ = "tbl_addresses"

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

    id = Column(Integer, primary_key=True)
    street_number = Column(String())
    street_type = Column(String())
    street_name = Column(String())
    direction = Column(String())
    city = Column(String(), default="Montreal")
    zip_code = Column(String())
    province = Column(String())
    region = Column(String())
    country = Column(String())
    business_id = Column(Integer, ForeignKey('tbl_businesses.id'),
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


class BusinessHour(Base):
    __tablename__ = "tbl_business_hours"

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

    id = Column(Integer, primary_key=True)
    day = Column(String(), nullable=False)
    closing_time = Column(Time, nullable=False, default=datetime.utcnow())
    opening_time = Column(Time, nullable=False, default=datetime.utcnow())
    business_id = Column(Integer, ForeignKey("tbl_businesses.id"))

    def __repr__(self):
        return '<BusinessHour {}: {} to {}>'.format(self.day, self.opening_time, self.closing_time)

    def __eq__(self, other):
        if not isinstance(other, BusinessHour):
            return False

        return self.day == other.day and \
               self.closing_time == other.closing_time and \
               self.opening_time == other.opening_time


class Phone(Base):
    __tablename__ = "tbl_phones"

    """
        Phone model
    """

    class Type(Enum):
        tel = "telephone"
        fax = "fax"

        @staticmethod
        def list():
            return [e.value for e in Phone.Type]

    id = Column(Integer, primary_key=True)
    number = Column(String(), nullable=False)
    extension = Column(String(), nullable=False)
    type = Column(String(), default=Type.tel.value)
    business_id = Column(Integer, ForeignKey('tbl_businesses.id'),
                            nullable=False)

    def __eq__(self, other):
        if not isinstance(other, Phone):
            return False

        return self.number == other.number and \
               self.extension == other.extension and \
               self.type == other.type

    def __repr__(self):
        return '<Phone: {}'.format(self.number)


class SocialLink(Base):
    __tablename__ = "tbl_social_links"

    class TypeEnum(Enum):
        instragram = "Instagram"
        facebook = "Facebook"
        linkedin = "LinkedIn"
        snapchat = "Snapchat"
        twitter = "Twitter"

        @staticmethod
        def list():
            return [e.value for e in SocialLink.TypeEnum]

    id = Column(Integer, primary_key=True)
    link = Column(String(), nullable=False)
    type = Column(String())
    business_id = Column(Integer, ForeignKey('tbl_businesses.id'), nullable=False)

    def __eq__(self, other):
        if not isinstance(other, SocialLink):
            return False

        return self.link == other.link and \
               self.type == other.type
