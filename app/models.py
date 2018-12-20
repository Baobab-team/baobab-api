from werkzeug.security import generate_password_hash, check_password_hash

# Define a base model for other database tables to inherit
from app import db
from marshmallow_sqlalchemy import ModelSchema


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


# Define base user

class User(db.Model):
    """
    User model
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    password = db.Column(db.String(128))

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User id={},email={}>'.format(self.id, self.email)


class Business(db.Model):
    """
    Business model
    """
    __tablename__ = 'business'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    phone = db.Column(db.String())
    email = db.Column(db.String())

    # addresses = db.relationship('Address', backref='business', lazy=True, uselist=False)
    # business_hours = db.relationship('BusinessHours', backref='business', lazy=True)

    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def __repr__(self):
        return '<id {}>'.format(self.name)


class BusinessSchema(ModelSchema):
    class Meta:
        model = Business

# class Address(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#
#     def __repr__(self):
#         return '<Address id {}>'.format(self.id)
#
#
# class Business(db.Model):
#     pass
