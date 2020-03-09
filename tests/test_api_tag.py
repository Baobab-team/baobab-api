import unittest

from app.businesses.models import Tag
from app import create_app, db
from app.config import TestingConfig


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config=TestingConfig)
        self.client = self.app.test_client

        self.tags = [Tag(**{"name": "Tag{}".format(i)}) for i in range(10)]

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.drop_all()

            db.create_all()
            [db.session.add(tag) for tag in self.tags]
            db.session.commit()

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def test_post(self):
        # Add business
        res = self.client().post('/api_v1/tags', json={"name": "LOL"})
        self.assertEqual(201, res.status_code)
        self.assertIn('LOL', str(res.data))

    def test_put(self):
        # Add business
        res = self.client().put('/api_v1/tags/1', json={"name": "Another tag"})
        self.assertEqual(200, res.status_code)
        self.assertIn('Another tag', str(res.data))

    def test_get(self):
        # Add business
        res = self.client().get('/api_v1/tags')
        self.assertEqual(200, res.status_code)
        self.assertIn('Tag1', str(res.data))
        self.assertIn('Tag3', str(res.data))
        self.assertIn('Tag9', str(res.data))


if __name__ == '__main__':
    unittest.main()
