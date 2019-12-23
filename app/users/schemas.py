from marshmallow import Schema, post_load, fields, validates, ValidationError

from app.users.models import User


class UserCreateSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    name = fields.String(required=False)
    type = fields.String(required=True)

    @validates('type')
    def validate_type(self, value):
        if value not in ['owner','customer']:
            raise ValidationError('Invalid user type')

    @post_load
    def make_object(self, data, **kwargs):
        return User(**data)


class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    name = fields.String(required=False)

    @post_load
    def make_object(self, data,**kwargs):
        return User(**data)


class UserUpdateSchema(Schema):
    password = fields.String(required=True)
    name = fields.String(required=False)
