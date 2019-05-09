# Define User data-model
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.common.base import Base


class User(Base):
    __tablename__ = 'user'

    # User Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    _password = db.Column(db.String(255), nullable=False)

    # User fields
    active = db.Column(db.Boolean, default=True)
    super = db.Column(db.Boolean, default=False)
    staff = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return '<User {}>'.format(self.email)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, pw):
        self._password = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self._password, pw)

    @staticmethod
    def create_superuser(email, password):
        user = User(email=email)
        user.password = password
        user.super = True

        try:
            user.save()
            return user

        except IntegrityError:
            raise ValueError("User with email already exist")


class EndUser(User):
    favorite_business = db.relationship('FavoriteBusiness', backref='user', lazy=True)


class OwnerUser(User):
    business = db.relationship('Business', backref='user', lazy=True)


class DataClerkUser(User):
    pass
