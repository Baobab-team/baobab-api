import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)
api = Api(app,"/api")

@app.route("/")
def index():
    return "Hello world"


from app.models import *
db.create_all()
from app.resources import BusinessResource

api.add_resource(BusinessResource,"/business/","/business/id")

# from app import models,resources
if __name__ == '__main__':
    app.run()



