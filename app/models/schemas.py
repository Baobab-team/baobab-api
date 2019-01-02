from marshmallow_sqlalchemy import ModelSchema

from app.models.business import Category, Business, Address, BusinessHour, Rating, FavoriteBusiness


class CategorySchema(ModelSchema):
    class Meta:
        model = Category
        exclude = ("businesses",)


class BusinessSchema(ModelSchema):
    class Meta:
        model = Business
        exclude = ("created","updated","accepted","notes",)



class AddressSchema(ModelSchema):
    class Meta:
        model = Address


class BusinessHourSchema(ModelSchema):
    class Meta:
        model = BusinessHour


class RatingSchema(ModelSchema):
    class Meta:
        model = Rating


class FavoriteSchema(ModelSchema):
    class Meta:
        model = FavoriteBusiness
