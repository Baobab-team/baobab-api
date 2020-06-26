import pytest
from werkzeug.exceptions import NotFound

from app.businesses.models import Category
from app.businesses.repositories import BaseRepository


def test_repository_query(app, _db):
    repository = BaseRepository()
    with pytest.raises(Exception):
        assert repository.query


def test_repository_get_strict(app, _db):
    repository = BaseRepository()
    repository.model = Category
    with pytest.raises(NotFound):
        assert repository.get(100, error_message="shit", strict=True)


def test_repository_filter(app, _db, category1):
    repository = BaseRepository()
    repository.model = Category
    categories = repository.filter(**{"name":category1.name}).all()
    assert len(categories) == 1
    assert categories[0].name == category1.name

def test_repository_save(app, _db):
    repository = BaseRepository()
    repository.model = Category
    category = Category(name="BarberShop",id=10)
    created_category = repository.save(category)
    assert created_category.id is not None
    assert created_category.name == "BarberShop"

def test_repository_update(app, _db,category1):
    repository = BaseRepository()
    repository.model = Category
    updated_category = repository.update(**{"name":"Brand new name"})
    assert updated_category.name == "Brand new name"