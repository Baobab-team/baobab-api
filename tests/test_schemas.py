from datetime import time

import pytest

from app.businesses.schemas import *


class TestBaseSchema(object):

    def test_valid_base_schema(self):
        data = {

        }
        assert BaseSchema().validate(data=data) == {}

    def test_base_unknown_field_exclusion(self):
        data = {
            "name": "fail",
        }
        assert BaseSchema().validate(data=data) == {}


class TestCategory(object):

    @pytest.mark.parametrize("id, name", [
        (1,"Category1"),
        (2,"Category2"),
        (3,"Category3"),
    ], ids=["T1", "T2", "T3"])
    def test_valid_category(self, id, name):
        data = {
            "name": name,
            "id": id,
        }
        assert CategorySchema().validate(data=data) == {}

    @pytest.mark.parametrize("name", [
        (10),
    ], ids=["T1", ])
    def test_invalid_category(self, name):
        data = {
            "name": name,
        }
        assert CategorySchema().validate(data=data) != {}


class TestBusiness(object):

    def test_valid_business(self):
        data = {
            "name": "Restaurant name",
            "description": "Restaurant desc",
            "website": "resto.com",
            "email": "john.doe@gmail.com",
            "notes": "notes",
            "category": {
                "id": "100",
                "name": "resto"
            },
            "owner_id": 1,
            "capacity": 120,
            "business_hours": [
                {
                    "day": "thursday",
                    "closing_time": time().isoformat(),
                    "opening_time": time().isoformat(),
                },
                {
                    "day": "monday",
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
            "social_links": [
                {"link": "facebook.com", "type": "Twitter"}
            ],
            "payment_types": ["cash"],
            "tags": [
                {"name": "Tag1", },
                {"name": "Tag2", }
            ]
        }
        assert BusinessCreateSchema().validate(data=data) == {}


class TestTags(object):
    @pytest.mark.parametrize("name", [
        ("tag1"),
        ("tag2"),
        ("tag3"),
    ], ids=["T1", "T2", "T3"])
    def test_valid_tags(self, name):
        data = {
            "name": name,
        }
        assert TagSchema().validate(data=data) == {}

    @pytest.mark.parametrize("name", [
        (None),
        (10),
    ], ids=["None", "integer"])
    def test_valid_tags(self, name):
        data = {
            "name": name,
        }
        assert TagSchema().validate(data=data) != {}


class TestBusinessHours(object):

    @pytest.mark.parametrize("day, opening_time, closing_time", [
        ("monday", time(10, 10, 10), time(20, 20, 0)),
        ("thursday", time(10, 10, 10), time(20, 20, 0)),
    ])
    def test_valid_business_hour(self, day, opening_time, closing_time):
        data = {
            "day": day,
            "opening_time": opening_time.isoformat(),
            "closing_time": closing_time.isoformat(),
        }
        assert BusinessHourSchema().validate(data=data) == {}

    @pytest.mark.parametrize("day, opening_time, closing_time", [
        ("None", time(10, 10, 10), time(20, 20, 0)),
        ("", time(10, 10, 10), time(22, 20, 0)),
    ])
    def test_invalid_business_hour(self, day, opening_time, closing_time):
        data = {
            "day": day,
            "opening_time": opening_time.isoformat(),
            "closing_time": closing_time.isoformat(),
        }
        assert BusinessHourSchema().validate(data=data) != {}


class TestPhoneSchema(object):

    @pytest.mark.parametrize("number, extension, type", [
        ("5147545588", "56", "fax"),
        ("514", "123", "telephone"),
    ])
    def test_valid_phone(self, number, extension, type):
        data = {
            "number": number,
            "extension": extension,
            "type": type,
        }
        assert PhoneSchema().validate(data=data) == {}

    @pytest.mark.parametrize("number, extension, type", [
        (12323123, None, "fax"),
        (None, 213213123, "telephone"),
        ("514", 213213123, "telephone"),
        (None, 213213123, "loll"),
    ])
    def test_invalid_phone(self, number, extension, type):
        data = {
            "number": number,
            "extension": extension,
            "type": type,
        }
        assert PhoneSchema().validate(data=data) != {}
