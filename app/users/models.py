from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.exc import IntegrityError

from  app.businesses.models import favorites
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    """
    User model
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)

    # User Authentication fields
    email = db.Column(db.String(255), nullable=False, unique=True)
    _password = db.Column(db.String(255), nullable=False)

    # User fields
    name = db.Column(db.String(), nullable=True)

    active = db.Column(db.Boolean, default=True)
    super = db.Column(db.Boolean, default=False)
    staff = db.Column(db.Boolean, default=False)
    type = db.Column(db.String(50))

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

        return user

    @property
    def access_token(self):
        return create_access_token(identity=self.email)

    @property
    def refresh_token(self):
        return create_refresh_token(identity=self.email)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }


class Customer(User):
    """
    Customer model
    """
    __tablename__ = 'customer'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    favorites = db.relationship('Favorite', secondary=favorites, lazy='subquery',
                           backref=db.backref('customer', lazy=True))

    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }


class Owner(User):
    """
    Owner model
    """
    __tablename__ = 'owner'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    business = db.relationship('Business', backref='owner', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'owner',
    }


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
