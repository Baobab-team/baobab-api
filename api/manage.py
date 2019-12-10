import os

from flask.cli import FlaskGroup
from app import create_app,db

config = os.getenv('APP_SETTINGS')  # config_name = config.DevelopmentConfig

app = create_app()

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()
