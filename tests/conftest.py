import pytest

from app import db, create_app
from app.businesses.models import Business, Category
from app.businesses.repositories import BusinessRepository
from app.config import TestingConfig


@pytest.yield_fixture()
def test_client():
    flask_app = create_app(config=TestingConfig)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()
@pytest.yield_fixture()
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    yield db  # this is where the testing happens!

    db.drop_all()

    db.session.close()

@pytest.fixture()
def category1():
    category1 = Category(name="restaurant",id=1)
    db.session.add(category1)
    db.session.flush()
    return category1
