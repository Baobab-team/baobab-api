from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Api, abort

from app.businesses import resources as res
from app.businesses.models import Business
from app.businesses.repositories import BusinessRepository
from app.businesses.schemas import BusinessSchema
from app.utils.decorators import marshal_with

blueprint = Blueprint("api_v1", __name__, url_prefix="/api_v1")

business_repository = BusinessRepository()


@blueprint.route('/businesses/<int:id_>/processStatus', methods=['PUT'])
@marshal_with(BusinessSchema, success_code=200)
def processStatus(id_):
    business = business_repository.get(id_)
    data = request.get_json()

    if "status" not in data:
        abort(400, message="Bad request")

    new_status = data["status"]
    if new_status in Business.StatusEnum.list():
        business.process_status(new_status)
        business_repository.save(business)
    else:
        abort(400, message="Invalid status")

    return business


api = Api(blueprint)

api.add_resource(res.BusinessCollection, "/businesses")
api.add_resource(res.BusinessScalar, "/businesses/<int:id>")
api.add_resource(res.BusinessTagCollection, "/businesses/<int:id>/tags")
api.add_resource(res.BusinessTagScalar, "/businesses/<int:id>/tags/<int:tag_id>")

api.add_resource(res.CategoriesCollection, "/categories")
api.add_resource(res.CategoryScalar, "/categories/<int:id>")

api.add_resource(res.TagCollection, "/tags")
api.add_resource(res.TagScalar, "/tags/<int:id>")

api.add_resource(res.UserCollection, "/users")
api.add_resource(res.UserScalar, "/users/<int:id>")
api.add_resource(res.UserRegistration, "/auth/register")
api.add_resource(res.UserLogin, "/auth/login")
api.add_resource(res.UserLogoutAccess, "/auth/logout/access")
api.add_resource(res.UserLogoutRefresh, "/auth/logout/refresh")
api.add_resource(res.UserTokenRefresh, "/auth/token/refresh")

