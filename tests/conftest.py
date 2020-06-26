import pytest

from app import db, create_app
from app.businesses.models import Business, Category
from app.businesses.repositories import BusinessRepository
from app.config import TestingConfig


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope='session')
def app():
    _app = create_app(config=TestingConfig)
    ctx = _app.app_context()
    ctx.push()
    yield _app
    ctx.pop()


@pytest.fixture(scope="session")
def _db(app):
    """
    Returns session-wide initialised database.
    """
    db.drop_all()
    db.create_all()
    yield db
# @pytest.yield_fixture()
# def test_client():
#     app = create_app(config=TestingConfig)
#     with app.test_client() as client:
#         yield client
# @pytest.yield_fixture()
# def init_database(test_client):
#     # Create the database and the database table
#     db.create_all()
#
#     yield db  # this is where the testing happens!
#
#     db.drop_all()
#
#     db.session.close()

@pytest.fixture()
def category1():
    category1 = Category(name="restaurant")
    db.session.add(category1)
    db.session.flush()
    return category1
