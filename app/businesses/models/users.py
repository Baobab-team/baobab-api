from enum import Enum

from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.businesses.models import BaseModel


class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    _password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(), nullable=True)
    last_name = db.Column(db.String(), nullable=True)
    active = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)

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
    def create_admin_user(email, password, firstname="", lastname=""):
        user = User(email=email, first_name=firstname, last_name=lastname)
        user.password = password

        return user

    @property
    def access_token(self):
        return create_access_token(identity=self.email)

    @property
    def refresh_token(self):
        return create_refresh_token(identity=self.email)


class Role(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    permissions = db.relationship('Permission', backref='role', lazy=True)


class Permission(BaseModel):
    class ActionEnum(Enum):
        edit = "edit"
        create = "create"
        view = "view"
        delete = "delete"

        @staticmethod
        def list():
            return [e.value for e in Permission.ActionEnum]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    action = db.Column(db.String(), nullable=False)


class RevokedTokenModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        revoked_token = cls.query.filter_by(jti=jti).first()
        return bool(revoked_token)
