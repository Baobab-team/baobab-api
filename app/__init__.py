import os
from logging.config import fileConfig
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import import_string

from app.config import TestingConfig

DEVELOPMENT_CONFIG = "app.config.DevelopmentConfig"
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yml'
LOGGING_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "logging.cfg")
LOGS_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config=os.getenv("APP_SETTINGS", DEVELOPMENT_CONFIG)):
    app = Flask(__name__)

    if config != TestingConfig:
        fileConfig(LOGGING_CONFIG_PATH)  # Configure logging

    @app.route("/")
    def index():
        return "If you are seeing this, it means the setup went well !"

    if isinstance(config, str):
        cfg = import_string(config)
        app.config.from_object(cfg())
    else:
        app.config.from_object(config)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize models
    from .businesses.models import Business, BusinessHour, Category, Address, Plate, Restaurant
    from .businesses.blueprints import blueprint as business_blueprint
    app.register_blueprint(business_blueprint)

    # Configure api documentation
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Baobab API documentation"},
    )
    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

    if not os.path.isdir(LOGS_FOLDER_PATH):
        os.mkdir(LOGS_FOLDER_PATH)

    return app



