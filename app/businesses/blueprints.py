from flask import Blueprint, request
from flask_restful import Api

from app.businesses import resources as res
from app.businesses.repositories import BusinessRepository
from app.businesses.schemas import BusinessSchema
from app.utils.decorators import marshal_with

blueprint = Blueprint("api_v1", __name__, url_prefix="/api_v1")

business_repository = BusinessRepository()


@blueprint.route('/businesses/<int:id_>/accept', methods=['PUT'])
@marshal_with(BusinessSchema, success_code=200)
def accept_business(id_):
    business = business_repository.get(id_)
    data = request.get_json()
    if data["accept"]:
        business.accept()
    else:
        business.refuse()

    business_repository.save(business)

    return business


api = Api(blueprint)

api.add_resource(res.BusinessCollection, "/businesses")
api.add_resource(res.BusinessScalar, "/businesses/<int:id>")

api.add_resource(res.CategoriesCollection, "/categories")
api.add_resource(res.CategoryScalar, "/categories/<int:id>")

