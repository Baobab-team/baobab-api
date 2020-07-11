import os
from dotenv import load_dotenv
from flask import Flask,_app_ctx_stack
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from sqlalchemy.orm import scoped_session
from werkzeug.utils import import_string

from logging.config import fileConfig

from .config import TestingConfig
from .database import  engine, db_session

DEVELOPMENT_CONFIG = "app.config.DevelopmentConfig"
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yml'
LOGGING_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "logging.cfg")
LOGS_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
load_dotenv()


UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))

if not os.path.isdir(LOGS_FOLDER_PATH):
    os.mkdir(LOGS_FOLDER_PATH)

def create_app(config=os.getenv("APP_SETTINGS", DEVELOPMENT_CONFIG)):
    app = Flask(__name__)

    if config != TestingConfig:
        fileConfig(LOGGING_CONFIG_PATH)  # Configure logging

    # Configure api documentation
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Baobab API documentation"
        },
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    @app.route("/")
    def hello_world():
        return "If you are seeing this, it means the setup went well !"

    if isinstance(config, str):
        cfg = import_string(config)
        app.config.from_object(cfg())

    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    # Initialize models
    from .businesses.models import Business, BusinessHour, Category, Address
    # Initialize API
    from .businesses.blueprints import blueprint as business_blueprint
    app.register_blueprint(business_blueprint)

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    app.session = scoped_session(db_session,scopefunc=_app_ctx_stack.__ident_func__)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        app.session.remove()
    return app
