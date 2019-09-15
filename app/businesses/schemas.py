from marshmallow import Schema, fields, post_load

from .models import Category, Business


class CategoryCreateSchema(Schema):
    name = fields.String()

    @post_load
    def make_object(self, data):
        return Category(**data)


class CategoryUpdateSchema(Schema):
    name = fields.String()


class CategorySchema(Schema):
    id = fields.String(required=False)
    name = fields.String(required=True)

    @post_load
    def make_object(self, data):
        return Category(**data)


class BusinessCreateSchema(Schema):
    category_id = fields.Integer(required=True)
    owner_id = fields.Integer(required=False)
    name = fields.String(required=True)
    description = fields.String(required=True)
    website = fields.String(required=False)
    notes = fields.String(required=False)
    email = fields.Email(required=False)

    @post_load
    def make_object(self, data):
        return Business(**data)


class BusinessUpdateSchema(Schema):
    category_id = fields.Integer()
    owner_id = fields.Integer()
    name = fields.String()
    description = fields.String()
    website = fields.String()
    email = fields.Email()


class BusinessSchema(Schema):
    id = fields.String(required=True)
    category_id = fields.String(required=True)
    owner_id = fields.String(required=False)
    name = fields.String(required=True)
    description = fields.String(required=True)
    website = fields.String()
    email = fields.Email()

    @post_load
    def make_object(self, data):
        return Business(**data)

