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
    @pytest.mark.parametrize("name, phone, description, website, email, accepted, notes,category_id,owner_id", [
        ("Name","111111111","Lorem ipsum","site.web.com","john.doe@email.com",True,"Notes....",1,1),
        ("Name","111111111","Lorem ipsum","site.web.com","john.doe@email.com",True,"Notes....",1,None)
    ], ids=["T1","T2"])
    def test_valid_business(self, name, phone, description, website, email, accepted, notes,category_id,owner_id):
        data = {
            "name": name,
            "phone": phone,
            "description": description,
            "website": website,
            "email": email,
            "accepted": accepted,
            "notes": notes,
            "category_id": 1,
            "owner_id": 1,
        }
        assert BusinessCreateSchema().validate(data=data) == {}
