import pytest

from api.app.businesses.schemas import *


class TestSchemas(object):

    @pytest.mark.parametrize("name", [
        ("Category1"),
        ("Category2"),
        ("Category3"),
    ], ids=["T1", "T2", "T3"])
    def test_valid_category_schema(self, name):
        data = {
            "name": name,
        }
        assert CategoryCreateSchema().validate(data=data) == {}

    @pytest.mark.parametrize("name", [
        (10),
    ], ids=["T1", ])
    def test_invalid_category_schema(self, name):
        data = {
            "name": name,
        }
        assert CategoryCreateSchema().validate(data=data) != {}


class TestBusiness(object):
    @pytest.mark.parametrize("name, phone, description, website, email, notes,category_id,owner_id", [
        ("Name", "111111111", "Lorem ipsum", "site.web.com", "john.doe@email.com",  "Notes....", 1, 1),
        ("Name", "111111111", "Lorem ipsum", "site.web.com", "john.doe@email.com",  "Notes....", 1, 1)
    ], ids=["T1", "T2"])
    def test_valid_business_schema(self, name, phone, description, website, email, notes, category_id,
                                   owner_id):
        data = {
            "name": name,
            "phone": phone,
            "description": description,
            "website": website,
            "email": email,
            "notes": notes,
            "category_id": category_id,
            "owner_id": owner_id,
        }
        assert BusinessCreateSchema().validate(data=data) == {}
