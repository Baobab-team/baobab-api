from marshmallow import Schema, fields, post_load, EXCLUDE, validates_schema, ValidationError
from marshmallow.validate import OneOf

from .models import Category, Business, SocialLink, Address, BusinessHour, Phone, Tag


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE


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
    prefix = fields.String(required=False)
    number = fields.String(required=True)
    extension = fields.String(required=False)
    type = fields.String(required=True, validate=OneOf(Phone.Type.list()))


class CategoryUpdateSchema(BaseSchema):
    name = fields.String()

    @post_load()
    def lower_name(self, item, many, **kwargs):
        item['name'] = item['name'].lower()
        return item


class CategorySchema(BaseSchema):
    id = fields.Integer(allow_none=True)
    name = fields.String(required=True)

    @post_load()
    def lower_name(self, item, many, **kwargs):
        item['name'] = item['name'].lower()
        return item

    @post_load
    def make_object(self, data, **kwargs):
        return Category(**data)


class PlateSchema(BaseSchema):
    id = fields.Integer(allow_none=True)
    name = fields.String(required=True)
    description = fields.String(required=False)
    price = fields.Float(required=True)


class MenuSchema(BaseSchema):
    id = fields.Integer(allow_none=True)
    name = fields.String(required=True)
    start = fields.Date(required=True)
    end = fields.Date(allow_none=True)
    plates = fields.List(fields.Nested(PlateSchema))

    @validates_schema
    def validate_dates(self, data, **kwargs):
        if data["end"] and data["start"] > data["end"]:
            raise ValidationError("End date must be greater then start date")


class RestaurantSchema(BaseSchema):
    id = fields.Integer(allow_none=True)
    menus = fields.List(fields.Nested(MenuSchema))


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
    status = fields.String(required=False)
    capacity = fields.Integer(required=False)
    business_hours = fields.List(fields.Nested(BusinessHourSchema))
    addresses = fields.List(fields.Nested(AddressSchema))
    social_links = fields.List(fields.Nested(SocialLinkSchema))
    tags = fields.List(fields.Nested(TagSchema))
    payment_types = fields.List(fields.String())

    @post_load
    def make_business(self, data, **kwargs):
        self.process_category(data)
        self.process_restaurant(data)
        return Business(**data)

    def process_category(self, data):
        data["category_id"] = data["category"].id
        del data["category"]

    def process_restaurant(self, data):
        if "restaurant" in data:
            data["restaurant_id"] = data["restaurant"].id
            del data["restaurant"]


class BusinessUpdateSchema(BaseSchema):
    category = fields.Nested(CategorySchema)
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
    name = fields.String(required=True)
    description = fields.String(required=True)
    website = fields.String()
    email = fields.Email()
    phones = fields.List(fields.Nested(PhoneSchema))
    accepted_at = fields.String(required=False)
    status = fields.String(required=False)
    capacity = fields.Integer(required=False)
    restaurant = fields.Nested(BusinessHourSchema)
    business_hours = fields.List(fields.Nested(BusinessHourSchema))
    addresses = fields.List(fields.Nested(AddressSchema))
    social_links = fields.List(fields.Nested(SocialLinkSchema))
    tags = fields.List(fields.Nested(TagSchema))
    payment_types = fields.List(fields.String())

    @post_load
    def make_object(self, data, **kwargs):
        return Business(**data)


class BusinessUploadSchema(BaseSchema):
    id = fields.String(required=True)
    filename = fields.String(required=True)
    error_message = fields.String()
    success = fields.Boolean()
    created_at = fields.Date()
    deleted_at = fields.Date()
    businesses_count = fields.Method("get_businesses_count")
    businesses = fields.List(fields.Nested(BusinessSchema))

    def get_businesses_count(self, obj):
        return len(obj.businesses)