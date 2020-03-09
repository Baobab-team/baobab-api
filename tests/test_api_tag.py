import unittest

from app.businesses.models import Tag
from app import create_app, db
from app.config import TestingConfig


class MyTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config=TestingConfig)
        self.client = self.app.test_client

        self.tags = [Tag(**{"name": "Tag{}".format(i)}) for i in range(1,10)]

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
        res = self.client().post('/api_v1/tags', json={"name": "LOL"})
        self.assertEqual(201, res.status_code)
        self.assertIn('LOL', str(res.data))

    def test_put(self):
        res = self.client().put('/api_v1/tags/1', json={"name": "Another tag"})
        self.assertEqual(200, res.status_code)
        self.assertIn('Another tag', str(res.data))

    def test_get(self):
        res = self.client().get('/api_v1/tags')
        self.assertEqual(200, res.status_code)
        self.assertIn('Tag1', str(res.data))
        self.assertIn('Tag3', str(res.data))
        self.assertIn('Tag9', str(res.data))

    def test_get_one(self):
        res = self.client().get('/api_v1/tags/1')
        self.assertEqual(200, res.status_code)
        self.assertIn('Tag1', str(res.data))

    def test_delete(self):
        res = self.client().delete('/api_v1/tags/1')
        self.assertEqual(204, res.status_code)
        self.assertEqual("", res.data.decode("utf-8"))

if __name__ == '__main__':
    unittest.main()
