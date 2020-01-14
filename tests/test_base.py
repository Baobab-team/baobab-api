import unittest

from app.common.base import TimestampMixin


class MyTestCase(unittest.TestCase):
    def test_something(self):
        t = TimestampMixin()

        self.assertTrue(t.isActive())
        t.deactivate()
        self.assertFalse(t.isActive())


if __name__ == '__main__':
    unittest.main()
