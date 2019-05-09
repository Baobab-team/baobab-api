from flask import Blueprint
from flask_restful import Api

from app.businesses.resources import BusinessScalar, BusinessCollection, CategoryScalar, CategoriesCollection

blueprint = Blueprint("api_v1", __name__, url_prefix="/api_v1")

api = Api(blueprint)

api.add_resource(BusinessCollection, "/businesses")
api.add_resource(BusinessScalar, "/businesses/<int:id>")

api.add_resource(CategoriesCollection, "/categories")
api.add_resource(CategoryScalar, "/categories/<int:id>")
