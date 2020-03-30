import unittest

from app.businesses.models import TimestampMixin


class MyTestCase(unittest.TestCase):
    def test_something(self):
        t = TimestampMixin()

        self.assertTrue(t.is_active())
        t.deactivate()
        self.assertFalse(t.is_active())


if __name__ == '__main__':
    unittest.main()
