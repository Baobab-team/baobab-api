import pytest

from app.businesses.exceptions import BaseException, EntityNotFoundException, ConflictException


def base_exception():
    raise BaseException


def test_base_exception():
    with pytest.raises(BaseException):
        base_exception()


def entity_not_found_excetion():
    raise EntityNotFoundException


def test_not_found_exception():
    with pytest.raises(EntityNotFoundException):
        entity_not_found_excetion()


def conflict_exception():
    raise ConflictException


def test_conflict_exception():
    with pytest.raises(ConflictException):
        conflict_exception()
