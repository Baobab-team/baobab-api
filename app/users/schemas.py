from marshmallow import Schema, post_load, fields

from app.users.models import User


class UserCreateSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    name = fields.String(required=False)


    @post_load
    def make_object(self, data):
        return User(**data)


class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    name = fields.String(required=False)

    @post_load
    def make_object(self, data):
        return User(**data)


class UserUpdateSchema(Schema):
    password = fields.String(required=True)
    name = fields.String(required=False)
