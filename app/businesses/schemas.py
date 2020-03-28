from marshmallow import Schema, fields, post_load, RAISE
from marshmallow.validate import OneOf

from .models import Category, Business, SocialLink, Address, BusinessHour, Phone, Tag


class BaseSchema(Schema):
    class Meta:
        unknown = RAISE


class AddressSchema(BaseSchema):
    id = fields.String()
    street_number = fields.String(required=True)
    street_type = fields.String(required=True)
    street_name = fields.String(required=True)
    direction = fields.String(required=True, validate=OneOf(Address.DirectionEnum.list()))
    city = fields.String(required=True)
    zip_code = fields.String(required=True)
    province = fields.String(required=True, validate=OneOf(Address.ProvinceEnum.list()))
    region = fields.String(required=True)
    country = fields.String(required=True)


class SocialLinkSchema(BaseSchema):
    id = fields.Integer()
    link = fields.String(required=True)
    type = fields.String(required=True, validate=OneOf(SocialLink.TypeEnum.list()))


class TagSchemaCreateOrUpdate(BaseSchema):
    name = fields.String(required=True)


class TagSchema(BaseSchema):
    id = fields.String()
    name = fields.String(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Tag(**data)


class TagListSchema(BaseSchema):
    tags = fields.List(fields.Nested(TagSchema))


class BusinessHourSchema(BaseSchema):
    id = fields.Integer()
    day = fields.String(required=True, validate=OneOf(BusinessHour.DaysEnum.list()))
    opening_time = fields.Time(required=True)
    closing_time = fields.Time(required=True)


class PhoneSchema(BaseSchema):
    id = fields.Integer()
    number = fields.String(required=True)
    extension = fields.String(required=False)
    type = fields.String(required=True, validate=OneOf(Phone.Type.list()))


class CategoryCreateSchema(BaseSchema):
    name = fields.String()

    @post_load
    def make_object(self, data, **kwargs):
        return Category(**data)


class CategoryUpdateSchema(BaseSchema):
    name = fields.String()


class CategorySchema(BaseSchema):
    id = fields.Integer(required=False)
    name = fields.String(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        return Category(**data)


class BusinessCreateSchema(BaseSchema):
    name = fields.String(required=True)
    phones = fields.List(
        fields.Nested(PhoneSchema)
    )
    description = fields.String(required=False)
    website = fields.String(required=False)
    email = fields.Email(required=False)
    notes = fields.String(required=False)
    category = fields.Nested(CategorySchema, required=True)
    owner_id = fields.Integer(required=False)
    status = fields.String(required=False)
    capacity = fields.Integer(required=False)
    business_hours = fields.List(fields.Nested(BusinessHourSchema))
    addresses = fields.List(fields.Nested(AddressSchema))
    social_links = fields.List(fields.Nested(SocialLinkSchema))
    tags = fields.List(fields.Nested(TagSchema))
    payment_types = fields.List(fields.String())

    @post_load
    def make_business(self, data, **kwargs):
        return Business(**data)


class BusinessUpdateSchema(BaseSchema):
    category = fields.Nested(CategorySchema)
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
    payment_types = fields.List(fields.String())


class BusinessSchema(BaseSchema):
    id = fields.String(required=True)
    category = fields.Nested(CategorySchema)
    restaurant_id = fields.Integer(required=False)
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
    payment_types = fields.List(fields.String())

    @post_load
    def make_object(self, data, **kwargs):
        return Business(**data)
