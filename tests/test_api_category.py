import unittest

from app.businesses.models import Category
from app.config import TestingConfig
from app import create_app, db


class CategoryTestCase(unittest.TestCase):
    """This class represents the category test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config=TestingConfig)
        self.client = self.app.test_client
        self.category1 = {'name': 'Category1'}
        self.category2 = {'name': 'Category2'}
        c1 = Category(name="Restaurant")
        c2 = Category(name="Beauty Salon")
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()
            for model in [c1, c2]:
                db.session.add(model)
            db.session.commit()

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def test_post(self):
        """Test API can create a category (POST request)"""
        res = self.client().post('/api_v1/categories', json=self.category1)
        self.assertEqual( 201,res.status_code)
        self.assertIn('Category1', str(res.data))

    def test_get_collection(self):
        """Test API can get all categories (GET request)"""
        res = self.client().get('/api_v1/categories')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Restaurant', str(res.data))
        self.assertIn('Beauty Salon', str(res.data))

    def test_get_scalar(self):
        res = self.client().get('/api_v1/categories/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Restaurant', str(res.data))

    def test_put(self):
        res = self.client().put('/api_v1/categories/1', json={'name': 'New name'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('New name', str(res.data))

    def test_delete(self):
        res = self.client().delete('/api_v1/categories/1')
        self.assertEqual(res.status_code, 204)

    def test_invalid_delete(self):
        res = self.client().delete('/api_v1/categories/4')
        self.assertEqual(res.status_code, 404)
        self.assertIn('Category doesnt exist', str(res.data))
