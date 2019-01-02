import os

from dotenv import load_dotenv
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv()
login_manager = LoginManager()

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
from app.routes.admin import bp as admin_bp

app.register_blueprint(token)
app.register_blueprint(admin_bp)

from app.models.users import User,OwnerUser,EndUser

login_manager.init_app(app)

from app.admin import UserView, LogoutMenuLink, LoginMenuLink

admin = Admin(app, name='admin')
admin.add_menu_item(LogoutMenuLink)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User,"OwnerUser":OwnerUser}