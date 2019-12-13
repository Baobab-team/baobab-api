from flask import Blueprint
from flask_restful import Api

from app.businesses import resources as res

blueprint = Blueprint("api_v1", __name__, url_prefix="/api_v1")

api = Api(blueprint)

api.add_resource(res.BusinessCollection, "/businesses")
api.add_resource(res.BusinessScalar, "/businesses/<int:id>")

api.add_resource(res.CategoriesCollection, "/categories")
api.add_resource(res.CategoryScalar, "/categories/<int:id>")

