import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from .common.errors import page_not_found, page_error

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config=None):
    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return "If you arent seing this, it means the setup went well !"

    if config is None:
        app.config.from_envvar('APP_SETTINGS')  # config_name = "development"

    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    db.init_app(app)
    jwt.init_app(app)

    # Initialize models
    from .users.models import User, Customer, Owner, RevokedTokenModel
    from .businesses.models import Business, BusinessHour, Category, Rating, Address

    # Initialize API
    from .businesses.blueprints import blueprint as business_blueprint
    app.register_blueprint(business_blueprint)
    from .users.blueprints import blueprint as user_bp
    app.register_blueprint(user_bp)

    if app.debug == False:
        # Initliaze errors page

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/baobab.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Baobab startup')

        app.register_error_handler(500, page_error)
        app.register_error_handler(404, page_not_found)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    return app
