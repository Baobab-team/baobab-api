
from api.app.common.base import TimestampMixin


class TestBase(object):

    def test_timestamp_default(self):
        t = TimestampMixin()
        t.activate()
        assert t.activated == True

    def test_timestamp_deactivte(self, ):
        t = TimestampMixin()
        t.deactivate()
        assert t.activated == False

        t.activate()
        assert t.activated == True
