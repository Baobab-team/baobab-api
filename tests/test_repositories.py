import pytest
from werkzeug.exceptions import NotFound

from app.businesses.models import Category
from app.businesses.repositories import BaseRepository


def test_repository(test_client,init_database):
    repository = BaseRepository()
    with pytest.raises(Exception):
        assert repository.query


def test_repository_get_strict(test_client,init_database):
    repository = BaseRepository()
    repository.model = Category
    with pytest.raises(NotFound):
        assert repository.get(1,error_message="shit",strict=True)
