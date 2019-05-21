import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.common.errors import page_not_found, page_error

load_dotenv()

db = SQLAlchemy()


def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        config = os.getenv('APP_SETTINGS')  # config_name = "development"

    app.config.from_object(config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Initialize API
    from app.businesses.blueprints import blueprint as business_blueprint

    app.register_blueprint(business_blueprint)

    # Initialize token
    from app.routes.api import token
    app.register_blueprint(token)

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

    from app.common.users import User, OwnerUser, EndUser

    return app
