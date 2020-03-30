import logging
import os
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import import_string

from .common.errors import page_not_found, page_error

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app(config=None):
    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return "If you arent seing this, it means the setup went well !"

    if config is None:
        cfg = import_string(os.getenv("APP_SETTINGS"))
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

    if not app.debug:
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


    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    return app
