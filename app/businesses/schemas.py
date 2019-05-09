from marshmallow import Schema, fields, post_load

# from app.common.business import Address, BusinessHour, Rating, FavoriteBusiness, Business, Category
from .models import Category, Business


class CategoryCreateSchema(Schema):
    name = fields.String()

    @post_load
    def make_object(self, data):
        return Category(**data)


class CategoryUpdateSchema(Schema):
    name = fields.String()


class CategorySchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=False)

    @post_load
    def make_object(self, data):
        return Category(**data)


class BusinessCreateSchema(Schema):
    id = fields.String(required=True)
    category_id = fields.String(required=True)
    owner_id = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    website = fields.String()
    email = fields.Email()

    @post_load
    def make_object(self, data):
        return Business(**data)

#
# class AddressSchema(ModelSchema):
#     class Meta:
#         model = Address
#
#
# class BusinessHourSchema(ModelSchema):
#     class Meta:
#         model = BusinessHour
#
#
# class RatingSchema(ModelSchema):
#     class Meta:
#         model = Rating
#
#
# class FavoriteSchema(ModelSchema):
#     class Meta:
#         model = FavoriteBusiness
