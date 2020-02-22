from marshmallow import Schema, fields, post_load

from .models import Category, Business


class PhoneSchema(Schema):
    id = fields.Integer()
    number = fields.String()
    extension = fields.String()
    type = fields.String()


class CategoryCreateSchema(Schema):
    name = fields.String()

    @post_load
    def make_object(self, data, **kwargs):
        return Category(**data)


class CategoryUpdateSchema(Schema):
    name = fields.String()


class CategorySchema(Schema):
    id = fields.String(required=False)
    name = fields.String(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Category(**data)


class BusinessCreateSchema(Schema):
    name = fields.String(required=True)
    legal_name = fields.String(required=False)
    phones = fields.List(
        fields.Nested(PhoneSchema)
    )
    description = fields.String(required=True)
    website = fields.String(required=False)
    email = fields.Email(required=False)
    notes = fields.String(required=False)
    category_id = fields.Integer(required=True)
    owner_id = fields.Integer(required=False)
    status = fields.String(required=False)


    @post_load
    def make_business(self, data, **kwargs):
        return Business(**data)


class BusinessUpdateSchema(Schema):
    category_id = fields.Integer()
    owner_id = fields.Integer()
    name = fields.String()
    legal_name = fields.String()
    description = fields.String()
    website = fields.String()
    email = fields.Email()
    phones = fields.List(fields.Nested(PhoneSchema))


class BusinessSchema(Schema):
    id = fields.String(required=True)
    category_id = fields.String(required=True)
    owner_id = fields.String(required=False)
    name = fields.String(required=True)
    legal_name = fields.String(required=True)
    description = fields.String(required=True)
    website = fields.String()
    email = fields.Email()
    phones = fields.List(fields.Nested(PhoneSchema))
    accepted_at = fields.String(required=False)
    status = fields.String(required=False)

    @post_load
    def make_object(self, data, **kwargs):
        return Business(**data)

