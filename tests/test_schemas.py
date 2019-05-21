import pytest

from app.businesses.schemas import CategoryCreateSchema


class TestCategory(object):

    @pytest.mark.parametrize("name", [
        ("Business1"),
        ("Business2"),
        ("Business4"),
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
