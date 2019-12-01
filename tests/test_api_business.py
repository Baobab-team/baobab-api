import unittest

from config import TestingConfig
from run import create_app, db


class BusinessTestCase(unittest.TestCase):
    """This class represents the business test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config=TestingConfig)
        self.client = self.app.test_client

        self.category1 = {'name': 'Restaurant'}
        self.business1 = {
            'name': 'Gracia Afrika',
            'phone': '514-111-1111',
            'website': 'yolo.website.com',
            'description': 'THe coolest restaurant',
            'email': 'gracia.afrika@gmail.com',
            'notes': 'Lorem Ipsum',
            'category_id': 1,
        }
        self.business2 = {
            'name': 'Le Bled',
            'phone': '514-222-3333',
            'website': 'yolo2.website.com',
            'description': 'THe cooleet restaurant2',
            'email': 'le.bled@gmail.com',
            'notes': 'Lorem Ipsum',
            'category_id': 1,
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def test_business_add(self):
        """Test API can create a business (POST request)"""

        # Add category
        res = self.client().post('/api_v1/categories', json=self.category1)
        self.assertEqual(201, res.status_code)
        self.assertIn('Restaurant', str(res.data))

        # Add business
        res = self.client().post('/api_v1/businesses', json=self.business1)
        self.assertEqual(201, res.status_code)
        self.assertIn('Gracia Afrika', str(res.data))

    def test_get_all_business(self):
        # Add category
        res = self.client().post('/api_v1/categories', json=self.category1)
        self.assertEqual(201, res.status_code)
        self.assertIn('Restaurant', str(res.data))

        # Add business
        res = self.client().post('/api_v1/businesses', json=self.business1)
        self.assertEqual(201, res.status_code)
        self.assertIn('Gracia Afrika', str(res.data))

        # Add business
        # res = self.client().post('/api_v1/businesses', json=self.business2)
        # self.assertEqual(201, res.status_code)
        # self.assertIn('Le Bled', str(res.data))

        # Fetch business
        res = self.client().get('/api_v1/businesses')
        self.assertEqual(200, res.status_code)
        self.assertIn('Gracia Afrika', str(res.data))
        # self.assertIn('Le Bled', str(res.data))

    def test_business_update(self):
        """Test API can create a business (POST request)"""

        # Add category
        res = self.client().post('/api_v1/categories', json=self.category1)
        self.assertEqual(201, res.status_code)
        self.assertIn('Restaurant', str(res.data))

        # Add business
        res = self.client().post('/api_v1/businesses', json=self.business1)
        self.assertEqual(201, res.status_code)
        self.assertIn('Gracia Afrika', str(res.data))

        # Update business
        res = self.client().put('/api_v1/businesses/1', json={'name': 'New name'})
        self.assertEqual(200, res.status_code)
        self.assertIn('New name', str(res.data))

    def test_business_get(self):
        """Test API can create a business (POST request)"""

        # Add category
        res = self.client().post('/api_v1/categories', json=self.category1)
        self.assertEqual(201, res.status_code)
        self.assertIn('Restaurant', str(res.data))

        # Add business
        res = self.client().post('/api_v1/businesses', json=self.business1)
        self.assertEqual(201, res.status_code)
        self.assertIn('Gracia Afrika', str(res.data))

        # Fetch business
        res = self.client().get('/api_v1/businesses')
        self.assertEqual(200, res.status_code)
        self.assertIn('Gracia Afrika', str(res.data))

    def test_business_get_with_filter(self):
        """Test API can filter a business (GET request)"""

        # Add category
        res = self.client().post('/api_v1/categories', json=self.category1)
        self.assertEqual(201, res.status_code)
        self.assertIn('Restaurant', str(res.data))

        # Add business
        res = self.client().post('/api_v1/businesses', json=self.business1)
        self.assertEqual(201, res.status_code)
        self.assertIn('Gracia Afrika', str(res.data))

        # Fetch business
        res = self.client().get('/api_v1/businesses?description=coolest')
        self.assertEqual(200, res.status_code)
        self.assertIn('Gracia Afrika', str(res.data))

