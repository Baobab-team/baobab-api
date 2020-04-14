from flask import jsonify, request
from flask_jwt_extended import jwt_refresh_token_required, create_access_token, get_jwt_identity, get_raw_jwt, \
    jwt_required
from flask_restful import Resource, abort
from flask_restful.reqparse import Argument

from app.utils.decorators import parse_with, marshal_with, parse_request
from .models import Tag, Business, RevokedTokenModel
from .repositories import BusinessRepository, CategoryRepository, TagRepository, UserRepository
from .schemas import BusinessCreateSchema, CategorySchema, CategoryUpdateSchema, BusinessSchema, \
    BusinessUpdateSchema, TagSchema, TagSchemaCreateOrUpdate, UserSchema, UserTokenSchema
from ..consts import BUSINESS_PER_PAGE


class BusinessCollection(Resource):
    """
    Show a list of businesses and lets you add it
    """

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessCollection, self).__init__()
        self.repository = repository_factory()

    @parse_request(
        Argument("querySearch", type=str, store_missing=False),
        Argument("status", type=str, store_missing=False, action="append"),
        Argument("accepted_at", type=str, store_missing=False),
        Argument("order_by", type=str, choices=("name"), default='name'),
        Argument("order", type=str, choices=("ASC", "DESC"), default="ASC"),
        Argument("page", type=int, default=1),
        Argument("businessPerPage", type=int, default=BUSINESS_PER_PAGE),
    )
    @marshal_with(BusinessSchema, many=True, success_code=200)
    def get(self, page, businessPerPage, status=None, querySearch=None, accepted_at=None,  order=None,
            order_by=None,
             **kwargs):
        return self.repository.filter(
            querySearch=querySearch, accepted_at=accepted_at, status=status, order=order,
            order_by=order_by, **kwargs
        ).paginate(page, businessPerPage, False).items

    @parse_with(BusinessCreateSchema(), arg_name="entity")
    @marshal_with(BusinessSchema, success_code=201)
    def post(self, entity, **kwargs):
        if self.repository.exist(entity.id):
            abort(400, message="Business already exist")

        return self.repository.save(entity)


class BusinessScalar(Resource):

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessScalar, self).__init__()
        self.repository = repository_factory()

    @parse_with(BusinessUpdateSchema(), arg_name="entity")
    @marshal_with(BusinessSchema)
    def put(self, id, entity):
        return self.repository.update(id, **entity)

    @marshal_with(BusinessSchema)
    def get(self, id):
        return self.repository.query.filter_by(id=id).first_or_404(description='Business doesnt exist')

    def delete(self, id):
        self.repository.delete(id=id, error_message="Business doesnt exists")
        return None, 204


class BusinessTagCollection(Resource):

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessTagCollection, self).__init__()
        self.repository = repository_factory()

    @marshal_with(TagSchema, many=True)
    def get(self, id):
        business = self.repository.get(id, error_message="Business doesnt exist")
        return business.tags

    @parse_with(TagSchema(), many=True, arg_name="tags")
    @marshal_with(TagSchema, many=True, success_code=201)
    def post(self, id, tags, **kwargs):
        business = self.repository.get(id, error_message='Business doesnt exist')

        for tag in tags:
            tag.addBusinessTag(business)

        self.repository.save(business)
        return business.tags


class BusinessTagScalar(Resource):

    def __init__(self, repository_factory=BusinessRepository):
        super(BusinessTagScalar, self).__init__()
        self.repository = repository_factory()

    def delete(self, id, tag_id, **kwargs):
        business = self.repository.get(id, error_message='Business doesnt exist')
        tag = Tag.query.get(tag_id)
        tag.removeBusinessTag(business)

        self.repository.save(business)

        return None,204


class CategoryScalar(Resource):

    def __init__(self, repository_factory=CategoryRepository):
        super(CategoryScalar, self).__init__()
        self.repository = repository_factory()

    @parse_with(CategoryUpdateSchema(), arg_name="entity")
    @marshal_with(CategorySchema)
    def put(self, id, entity, **kwargs):
        return self.repository.update(id, **entity)

    def delete(self, id):

        # return proper status code
        if self.repository.delete(id):
            return None, 204
        else:
            return {"message": "Category doesnt exist"}, 404

    @marshal_with(CategorySchema)
    def get(self, id):
        return self.repository.query.filter_by(id=id).first_or_404(description='Category doesnt exist')


class CategoriesCollection(Resource):

    def __init__(self, repository_factory=CategoryRepository):
        super(CategoriesCollection, self).__init__()
        self.repository = repository_factory()

    @marshal_with(CategorySchema, many=True, success_code=200)
    def get(self):
        return self.repository.query.all()

    @parse_with(CategorySchema(), arg_name="entity")
    @marshal_with(CategorySchema, success_code=201)
    def post(self, entity, **kwargs):
        if self.repository.exist(entity.id):
            abort(400, message="Category already exist")

        return self.repository.save(entity)


class TagScalar(Resource):

    def __init__(self, repository_factory=TagRepository):
        super(TagScalar, self).__init__()
        self.repository = repository_factory()

    @parse_with(TagSchemaCreateOrUpdate(), arg_name="entity")
    @marshal_with(TagSchema)
    def put(self, id, entity, **kwargs):
        return self.repository.update(id, **entity)

    def delete(self, id):

        # return proper status code
        if self.repository.delete(id):
            return None, 204
        else:
            return {"message": "Tag doesnt exist"}, 404

    @marshal_with(TagSchema)
    def get(self, id):
        return self.repository.query.filter_by(id=id).first_or_404(description='Tag doesnt exist')


class TagCollection(Resource):

    def __init__(self, repository_factory=TagRepository):
        super(TagCollection, self).__init__()
        self.repository = repository_factory()

    @marshal_with(TagSchema, many=True, success_code=200)
    def get(self):
        return self.repository.query.all()

    @parse_with(TagSchema(), arg_name="entity")
    @marshal_with(TagSchema, success_code=201)
    def post(self, entity, **kwargs):
        if self.repository.exist(entity.id):
            abort(400, message="Tag already exist")

        return self.repository.save(entity)


class UserScalar(Resource):

    def __init__(self, repository_factory=UserRepository):
        super(UserScalar, self).__init__()
        self.repository = repository_factory()

    @parse_with(UserSchema(), arg_name="entity")
    @marshal_with(UserSchema)
    def put(self, id, entity):
        return self.repository.update(id, **entity)

    @marshal_with(UserSchema)
    def get(self, id):
        return self.repository.get(id)

    def delete(self, id):
        user = self.repository.get(id)
        # user.delete() # TODO update when function is created
        return None, 204


class UserCollection(Resource):

    def __init__(self, repository_factory=UserRepository):
        super(UserCollection, self).__init__()
        self.repository = repository_factory()

    @marshal_with(UserSchema, many=True, success_code=200)
    def get(self):
        return self.repository.query.all()


class UserRegistration(Resource):
    def __init__(self, repository_factory=UserRepository):
        super(UserRegistration, self).__init__()
        self.repository = repository_factory()

    @parse_with(UserSchema(), arg_name="entity")
    @marshal_with(UserTokenSchema, success_code=200)
    def post(self, entity, **kwargs):
        if self.repository.exist(entity.email):
            abort(400, message="User already exist")

        user = self.repository.save(entity)
        return user


class UserLogin(Resource):
    def __init__(self, repository_factory=UserRepository):
        super(UserLogin, self).__init__()
        self.repository = repository_factory()

    def post(self):
        email = request.authorization.username
        password = request.authorization.password

        user = self.repository.query.filter_by(email=email).first()

        if user:
            if user.active and user.check_password(password):
                return {
                    'message': 'User {} was created'.format(user.email),
                    'access_token': user.access_token,
                    'refresh_token': user.refresh_token
                }
            else:
                return {"message": "Email and password don't match"}, 401

        return jsonify({"message": "Something wrong happen"}), 500


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except Exception as err:
            return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}