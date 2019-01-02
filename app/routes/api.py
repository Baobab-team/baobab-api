from flask import jsonify, request, Blueprint
from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
from sqlalchemy.exc import IntegrityError

from app.models.users import User

token = Blueprint('token', __name__, url_prefix='/token')


@token.route('/register', methods=['POST'])
def register():
    email = request.authorization["username"]
    password = request.authorization["password"]

    user = User(email=email, password=password)

    try:
        user.save()
    except IntegrityError:
        return jsonify({"message": "User with email/user already exists"}), 401

    # Use create_access_token() and create_refresh_token() to create our
    # access and refresh tokens
    ret = {
        'access_token': create_access_token(identity=email),
        'refresh_token': create_refresh_token(identity=password)
    }
    return jsonify(ret), 200


@token.route('/login', methods=['POST'])
def login():
    email = request.authorization["username"]
    password = request.authorization["password"]

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"message": "Email and password don't match"}), 401

    # Use create_access_token() and create_refresh_token() to create our
    # access and refresh tokens
    ret = {
        'access_token': create_access_token(identity=email),
        'refresh_token': create_refresh_token(identity=email)
    }
    return jsonify(ret), 200


# The jwt_refresh_token_required decorator insures a valid refresh
# token is present in the request before calling this endpoint. We
# can use the get_jwt_identity() function to get the identity of
# the refresh token, and use the create_access_token() function again
# to make a new access token for this identity.
@token.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200


@token.route('/protected', methods=['GET'])
@jwt_required
def protected():
    username = get_jwt_identity()
    return jsonify(logged_in_as=username), 200
