import unittest

from api.app.config import TestingConfig
from run import create_app, db


class CategoryTestCase(unittest.TestCase):
    """This class represents the category test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config=TestingConfig)
        self.client = self.app.test_client
        self.category1 = {'name': 'Restaurant'}
        self.category2 = {'name': 'Beauty Salon'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_category_add(self):
        """Test API can create a category (POST request)"""
        res = self.client().post('/api_v1/categories', json=self.category1)
        self.assertEqual( 201,res.status_code)
        self.assertIn('Restaurant', str(res.data))

    def test_get_all_categories(self):
        """Test API can get all categories (GET request)"""
        res = self.client().post('/api_v1/categories', json=self.category1)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api_v1/categories', json=self.category2)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api_v1/categories')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Restaurant', str(res.data))
        self.assertIn('Beauty Salon', str(res.data))

    def test_category_get(self):
        """Test API can get a category (GET request)"""
        res = self.client().post('/api_v1/categories', json=self.category1)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api_v1/categories/1', json=self.category1)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Restaurant', str(res.data))

    def test_category_update(self):
        """Test API can update a category (PUT request)"""
        res = self.client().post('/api_v1/categories', json=self.category1)
        self.assertEqual(res.status_code, 201)
        res = self.client().put('/api_v1/categories/1', json={'name': 'New name'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('New name', str(res.data))

    def test_category_delete(self):
        """Test API can delete a category (DELETE request)"""
        res = self.client().post('/api_v1/categories', json=self.category1)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api_v1/categories/1', json=self.category1)
        self.assertEqual(res.status_code, 204)

    def test_category_invalid_delete(self):
        """Test API can delete a category (DELETE request) -- INVALID"""
        res = self.client().delete('/api_v1/categories/1')
        self.assertEqual(res.status_code, 404)
        self.assertIn('Category doesnt exist', str(res.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()
