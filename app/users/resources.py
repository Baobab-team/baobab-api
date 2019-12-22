from flask import jsonify
from flask_jwt_extended import jwt_required, get_raw_jwt, jwt_refresh_token_required, get_jwt_identity, \
    create_access_token
from flask_restful import Resource, abort, request

from app.users.models import RevokedTokenModel
from app.users.repositories import UserRepository
from app.users.schemas import UserCreateSchema, UserSchema, UserUpdateSchema
from app.utils.decorators import parse_with, marshal_with


class UserScalar(Resource):
    """
    Show user and lets you remove/add/update it
    """

    def __init__(self, repository_factory=UserRepository):
        super(UserScalar, self).__init__()
        self.repository = repository_factory()

    @parse_with(UserUpdateSchema(), arg_name="entity")
    @marshal_with(UserSchema)
    def put(self, id, entity):
        return self.repository.update(id, **entity)

    @marshal_with(UserSchema)
    def get(self, id):
        return self.repository.query.filter_by(id=id).first_or_404(description='User doesnt exist')

    def delete(self, id):
        # return proper status code
        self.repository.delete(id)
        return None, 204


class UserCollection(Resource):

    def __init__(self, repository_factory=UserRepository):
        super(UserCollection, self).__init__()
        self.repository = repository_factory()

    @marshal_with(UserSchema, many=True, success_code=200)
    def get(self):
        return self.repository.query.all()

    def delete(self, id):
        # return proper status code
        self.repository.delete(id)  # TODO Change for deactivate
        return None, 204


class UserRegistration(Resource):
    def __init__(self, repository_factory=UserRepository):
        super(UserRegistration, self).__init__()
        self.repository = repository_factory()

    @parse_with(UserCreateSchema(), arg_name="entity")
    def post(self, entity, **kwargs):
        if self.repository.exist(entity.email):
            abort(400, message="User already exist")

        user = self.repository.save(entity)
        return {
            'message': 'User {} was created'.format(user.email),
            'access_token': user.access_token,
            'refresh_token': user.refresh_token
        }


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

