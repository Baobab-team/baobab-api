from flask import jsonify, current_app
from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse, fields, marshal_with, abort, Api
from sqlalchemy.exc import IntegrityError

import app
from app.models.business import Business, Rating, FavoriteBusiness, Category
from app.models.schemas import BusinessSchema, RatingSchema, FavoriteSchema, CategorySchema

api = Api(prefix="/api")
business_parser = reqparse.RequestParser()
business_parser.add_argument("description", required=True, help="The description is required")
business_parser.add_argument("name", required=True, help="The name is required")
business_parser.add_argument("phone", required=True, help="The phone required")
business_parser.add_argument("category_id", required=True, help="The category id is required")

category_parser = reqparse.RequestParser()
category_parser.add_argument("name",required=True,help="The name is category")


rating_parser = reqparse.RequestParser()
rating_parser.add_argument("user_id", required=True, help="The user id")
rating_parser.add_argument("business_id", required=True, help="The business id")
rating_parser.add_argument("comment", required=True, help="The comment")
rating_parser.add_argument("rating", required=True, help="The rating")

favorite_parser = reqparse.RequestParser()
favorite_parser.add_argument("user_id", required=True, help="The user id")
favorite_parser.add_argument("business_id", required=True, help="The business id")
favorite_parser.add_argument("favorite")


class ProtectedResource(Resource):
    __abstract__ = True
    method_decorators = [jwt_required]


@api.resource("/categories/<int:id>")
class CategoryResource(ProtectedResource):
    """
    SHow a single category and lets you update it
    """

    def get(self, id):
        category = Category.query.filter_by(id=id).first_or_404()
        schema = CategorySchema(many=False)

        data = schema.dump(category).data
        return data, 201


@api.resource("/categories")
class CategoryResourceList(ProtectedResource):
    """
    SHow a list of categories and lets you update it
    """

    def get(self):
        categories = Category.query.all()
        schema = CategorySchema(many=True)

        data = schema.dump(categories).data
        return data, 201

    def post(self):
        args = category_parser.parse_args()
        name = args["name"]
        category = Category(name=name)
        try:
            category.save()
        except IntegrityError:
            abort(409, message="An error occured. Category couldnt be added",code=409)
        schema = CategorySchema(many=False)

        data = schema.dump(category).data
        return data, 201


@api.resource("/businesses/<int:id>")
class BusinessResource(Resource):
    """
    SHow a single business and lets you update it
    """

    def get(self, id):
        business = Business.query.filter_by(id=id).first_or_404()
        business_schema = BusinessSchema(many=False)

        data = business_schema.dump(business).data
        return data, 201

    def put(self, id):
        args = business_parser.parse_args()
        email = args["email"]
        phone = args["phone"]

        business = Business.query.filter_by(id=id).first()

        try:
            if business:
                business.phone = phone
                business.email = email
                business.save()
                business_schema = BusinessSchema(many=False)
                data = business_schema.dump(business).data
                return data
        except IntegrityError:
            return jsonify({"msg":"An error occured. Business couldnt be updated"})


@api.resource("/businesses")
class BusinessResourceList(Resource):
    """
    SHow a list of businesses and lets you add it
    """

    def get(self):
        list = Business.query.all()
        business_schema = BusinessSchema(many=True)
        data = business_schema.dump(list).data
        return data,200

    def post(self):
        args = business_parser.parse_args()
        description = args["description"]
        name = args["name"]
        phone = args["phone"]
        category_id = args["category_id"]

        try:

            business = Business.query.filter_by(name=name).first()
            if business:
                return jsonify({"msg":"Busines with name '{}' already exists".format(name)})

            business = Business(
                name=name,
                description=description,
                category_id=category_id,
                phone=phone
            )

            business.save()
            business_schema = BusinessSchema(many=False)
            data = business_schema.dump(business).data
            return data, 201
        except IntegrityError as e:
            print(str(e))
            return jsonify({"msg": "An error occured. Couldnt add the business"})


class FavoriteResourceList(ProtectedResource):
    """
    Show a list of favorite businesses or lets you add one
    """

    def post(self):
        args = favorite_parser.parse_args()
        business_id = args["business_id"]
        user_id = args["user_id"]
        favorite = args["favorite"]

        _favorite = FavoriteBusiness.query.filter_by(user_id=user_id, business_id=business_id).first()

        if not _favorite:
            _favorite = FavoriteBusiness(business_id=business_id, user_id=user_id, favorite=favorite)
            _favorite.save()
            schema = FavoriteSchema(many=False)
            data = schema.dump(favorite).data

            return jsonify({"favorites": data})


        else:
            return jsonify({"msg": "Favorite for business {}  from user {) doesn't exist".format(business_id, user_id)})

    def get(self):
        schema = FavoriteSchema(many=True)

        favorite_businesses = FavoriteBusiness.query.all()
        data = schema.dump(favorite_businesses).data

        return data, 200


class FavoriteResource(ProtectedResource):
    """
    Show a single favorite business and lets you delete, or update
    """

    def put(self, business_id, user_id):
        args = favorite_parser.parse_args()

        favorite = FavoriteBusiness.query.filter_by(user_id=user_id, business_id=business_id).first()

        if favorite:
            favorite.favorite = args["favorite"]
            favorite.save()
            schema = FavoriteSchema(many=False)
            favorite = FavoriteBusiness.query.all()
            data = schema.dump(favorite).data

            return data
        else:
            abort(404, message="Favorite for business {}  from user {) doesn't exist".format(business_id, user_id))

    def get(self, business_id, user_id):
        favorite = FavoriteBusiness.query.filter_by(user_id=user_id, business_id=business_id).first()

        if favorite:
            schema = FavoriteSchema(many=False)
            favorite = FavoriteBusiness.query.all()
            data = schema.dump(favorite).data

            return data, 200

    def delete(self, business_id, user_id):
        favorite = FavoriteBusiness.query.filter_by(user_id=user_id, business_id=business_id).first()

        if favorite:
            favorite.delete()

        else:
            abort(404, message="Favorite for business {}  from user {) doesn't exist".format(business_id, user_id))


@api.resource("/businesses/<int:id>/ratings")
class RatingResourceList(ProtectedResource):
    """
    Show list of ratings for a business or lets you add a rating
    """

    def post(self):
        args = rating_parser.parse_args()
        business_id = args["business_id"]
        user_id = args["user_id"]
        comment = args["comment"]
        rate = args["rate"]

        rating = Rating.query.filter_by(user_id=user_id, business_id=business_id).first()

        if not rating:
            rating = Rating(user_id=user_id, business_id=business_id, comment=comment, rate=rate)
            rating.save()
            schema = RatingSchema(many=False)

            data = schema.dump(rating).data
            return jsonify({"ratings": data})

        else:
            return jsonify({"msg": "Rating name already exist"})

    def get(self, business_id):
        schema = RatingSchema(many=True)

        ratings = Rating.query.filter_by(business_id=business_id).first()
        data = schema.dump(ratings).data

        return jsonify({"rating": data})


@api.resource("/businesses/<int:business_id>/ratings/<int:user_id>")
class RatingResource(ProtectedResource):
    """
    Show a single rating item and lets you delete it
    """

    def delete(self, business_id, user_id):
        rating = Rating.query.filter_by(business_id=business_id, user_id=user_id).first()

        if rating:
            rating.delete()
            return '', 204
        else:
            abort(404, message="Rating for business {}  from user {) doesn't exist".format(business_id, user_id))

    def get(self, business_id, user_id):
        rating = Rating.query.filter_by(business_id=business_id, user_id=user_id).first()

        if rating:
            schema = RatingSchema(many=False)

            data = schema.dump(rating).data

            return data, 200
        else:
            abort(404, message="Rating for business {}  from user {) doesn't exist".format(business_id, user_id))

    def put(self, business_id, user_id):
        args = rating_parser.parse_args()

        rating = Rating.query.filter_by(business_id=business_id, user_id=user_id).first()

        if rating:
            rating.comment = args["comment"]
            rating.rate = args["rate"]
            rating.save()

        else:
            abort(404, message="Rating for business {}  from user {) doesn't exist".format(business_id, user_id))
