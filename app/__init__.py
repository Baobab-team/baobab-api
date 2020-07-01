import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.utils import import_string
from logging.config import fileConfig

DEVELOPMENT_CONFIG = "app.config.DevelopmentConfig"
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yml'
LOGGING_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "logging.cfg")

load_dotenv()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config=os.getenv("APP_SETTINGS", DEVELOPMENT_CONFIG)):
    app = Flask(__name__)

    fileConfig(LOGGING_CONFIG_PATH) # Confugire logging

    # Configure api documentation
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Baobab API documentation"
        },
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route("/")
    def hello_world():
        return "If you are seeing this, it means the setup went well !"

    if isinstance(config, str):
        cfg = import_string(config)
        app.config.from_object(cfg())

    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize models
    from .businesses.models import Business, BusinessHour, Category, Address

    # Initialize API
    from .businesses.blueprints import blueprint as business_blueprint
    app.register_blueprint(business_blueprint)

    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    return app
