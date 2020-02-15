import pytest

from app.businesses.schemas import *


class TestCategory(object):

    @pytest.mark.parametrize("name", [
        ("Category1"),
        ("Category2"),
        ("Category3"),
    ], ids=["T1", "T2", "T3"])
    def test_valid_category(self, name):
        data = {
            "name": name,
        }
        assert CategoryCreateSchema().validate(data=data) == {}

    @pytest.mark.parametrize("name", [
        (10),
    ], ids=["T1", ])
    def test_invalid_category(self, name):
        data = {
            "name": name,
        }
        assert CategoryCreateSchema().validate(data=data) != {}


class TestBusiness(object):
    @pytest.mark.parametrize("name, description, website, email, notes,category_id,owner_id", [
        ("Name","Lorem ipsum","site.web.com","john.doe@gmail.com","Notes....",1,1),
        ("Name","Lorem ipsum","site.web.com","john.doe@gmail.com","Notes....",1,1)
    ], ids=["T1","T2"])
    def test_valid_business(self, name, description, website, email, notes,category_id,owner_id):
        data = {
            "name": name,
            "description": description,
            "website": website,
            "email": email,
            "notes": notes,
            "category_id": category_id,
            "owner_id": owner_id,
        }
        assert BusinessCreateSchema().validate(data=data) == {}
