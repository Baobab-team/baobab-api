from marshmallow import Schema, fields, post_load
from marshmallow.validate import OneOf

from .models import Category, Business, SocialLink, PaymentType, Address


class AddressSchema(Schema):
    id = fields.String()
    street_number = fields.String(required=True)
    street_type = fields.String(required=True)
    street_name = fields.String(required=True)
    direction = fields.String(required=True,validate=OneOf(Address.DirectionEnum.list()))
    city = fields.String(required=True)
    zip_code = fields.String(required=True)
    province = fields.String(required=True,validate=OneOf(Address.ProvinceEnum.list()))
    region = fields.String(required=True)
    country = fields.String(required=True)


class SocialLinkSchema(Schema):
    id = fields.Integer()
    link = fields.String(required=True)
    type = fields.String(required=True, validate=OneOf(SocialLink.TypeEnum.list()))


class TagSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)


class PaymentTypeSchema(Schema):
    id = fields.String(required=True)
    type = fields.String(required=True,validate=OneOf(PaymentType.TypeEnum.list()))


class BusinessHourSchema(Schema):
    id = fields.Integer()
    day = fields.String(required=True)
    opening_time = fields.Time(required=True)
    closing_time = fields.Time(required=True)


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
    capacity = fields.Integer(required=False)
    business_hours = fields.List(fields.Nested(BusinessHourSchema))
    addresses = fields.List(fields.Nested(AddressSchema))
    social_links = fields.List(fields.Nested(SocialLinkSchema))
    tags = fields.List(fields.Nested(TagSchema))
    payment_type = fields.List(fields.Nested(PaymentTypeSchema))

    @post_load
    def make_business(self, data, **kwargs):
        return Business(**data)


class BusinessUpdateSchema(Schema):
    category_id = fields.Integer()
    owner_id = fields.Integer()
    name = fields.String()
    description = fields.String()
    website = fields.String()
    email = fields.Email()
    phones = fields.List(fields.Nested(PhoneSchema))
    capacity = fields.Integer(required=False)
    business_hours = fields.List(fields.Nested(BusinessHourSchema))
    addresses = fields.List(fields.Nested(AddressSchema))
    social_links = fields.List(fields.Nested(SocialLinkSchema))
    tags = fields.List(fields.Nested(TagSchema))
    payment_type = fields.List(fields.Nested(PaymentTypeSchema))


class BusinessSchema(Schema):
    id = fields.String(required=True)
    category_id = fields.Integer(required=True)
    restaurant_id = fields.Integer(required=True)
    owner_id = fields.String(required=False)
    name = fields.String(required=True)
    description = fields.String(required=True)
    website = fields.String()
    email = fields.Email()
    phones = fields.List(fields.Nested(PhoneSchema))
    accepted_at = fields.String(required=False)
    status = fields.String(required=False)
    capacity = fields.Integer(required=False)
    business_hours = fields.List(fields.Nested(BusinessHourSchema))
    addresses = fields.List(fields.Nested(AddressSchema))
    social_links = fields.List(fields.Nested(SocialLinkSchema))
    tags = fields.List(fields.Nested(TagSchema))
    payment_type = fields.List(fields.Nested(PaymentTypeSchema))

    @post_load
    def make_object(self, data, **kwargs):
        return Business(**data)
