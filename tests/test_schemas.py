from datetime import datetime, time

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

    def test_valid_business(self):
        data = {
            "name": "Restaurant name",
            "description": "Restaurant desc",
            "website": "resto.com",
            "email": "john.doe@gmail.com",
            "notes": "notes",
            "category_id": 5,
            "owner_id": 1,
            "capacity": 120,
            "business_hours": [
                {
                    "day": "Monday",
                    "closing_time": time().isoformat(),
                    "opening_time": time().isoformat(),
                },
                {
                    "day": "Monday",
                    "closing_time": time(10, 30, 0).isoformat(),
                    "opening_time": time(18, 30, 0).isoformat(),
                }
            ],
            "addresses": [{
                "street_number": "2700",
                "street_name": "Kent",
                "street_type": "Street",
                "direction": "",
                "city": "Montreal",
                "zip_code": "H1h 0H0",
                "region": "",
                "country": "Canada",
                "province": "QC",
            }],
            "social_links" : [
                {"link":"facebook.com","type":"Twitter"}
            ],
            "tags": [
                {"name":"Tag1",},
                {"name":"Tag2",}
            ]
        }
        assert BusinessCreateSchema().validate(data=data) == {}
