import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# def create_app(test_config=None):
app = Flask(__name__)

app.config.from_object(os.getenv('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route("/")
def index():
    return "Hello world"


# Initialize API
from app.routes.resources import api

api.init_app(app)

# Initialize token
from app.routes.api import token

app.register_blueprint(token)

from app.models.users import User,OwnerUser,EndUser
from app.models.business import Business,Address,BusinessHour

from app.admin import admin




@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User,"OwnerUser":OwnerUser}