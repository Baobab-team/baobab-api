import os

from app import create_app, db
from flask.cli import  FlaskGroup
config = os.getenv('APP_SETTINGS')  # config_name = config.DevelopmentConfig
app = create_app(config)
# app.app_context().push()

cli = FlaskGroup(app)
if __name__ == '__main__':
    cli()
