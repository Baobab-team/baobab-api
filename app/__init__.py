import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# def create_app(test_config=None):
app = Flask(__name__)

app.config.from_object(os.getenv('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template('index.html', title='Home')


# Initialize API
from app.routes.resources import api

api.init_app(app)

# Initialize token
from app.routes.api import token

app.register_blueprint(token)

if app.debug == False:
    # Initliaze errors page
    from app.routes import errors

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


from app.models.users import User,OwnerUser,EndUser
from app.models.business import Business,Address,BusinessHour

from app.admin import admin




@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User,"OwnerUser":OwnerUser}