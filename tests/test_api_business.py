import unittest
import json

from app import create_app, db
from app.businesses.models import Category, Tag, Business
from app.businesses.schemas import BusinessSchema
from app.config import TestingConfig


class BusinessTestCase(unittest.TestCase):
    """This class represents the business test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config=TestingConfig)
        self.client = self.app.test_client

        self.category1 = {'name': 'Restaurant'}
        self.phone1 = {
            'id': 1,
            'number': '514-222-3333',
            'extension': '',
            'type': 'tel',
        }
        self.business1 = {
            'name': 'Gracia Afrika',
            'phones': [

            ],
            'website': 'yolo.website.com',
            'description': 'THe coolest restaurant',
            'email': 'gracia.afrika@gmail.com',
            'notes': 'Lorem Ipsum',
            'status': "pending",
            'category_id': 1,
            'tags': [
                {
                    'id': "1",
                    'name': "Tag1",
                }
            ]
        }
        self.business2 = {
            'name': 'Le Bled',
            'phones': [
                # self.phone1,
            ],
            'website': 'yolo2.website.com',
            'description': 'THe cooleet restaurant2',
            'email': 'le.bled@gmail.com',
            'notes': 'Lorem Ipsum',
            'category_id': 1,
        }

        category = Category(**self.category1)
        business = Business(name="business1", category_id="1")
        tag = Tag(name="Tag1")
        tag.addBusinessTag(business)

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.drop_all()
            db.create_all()
            db.session.add(category)
            db.session.commit()

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def setup_minimal_data(self, models):
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.drop_all()
            db.create_all()
            for model in models:
                db.session.add(model)
            db.session.commit()

    def test_business_add(self):
        """Test API can create a business (POST request)"""

        # Add business
        res = self.client().post('/api_v1/businesses', json=self.business2)
        self.assertEqual(201, res.status_code)
        self.assertIn('Le Bled', str(res.data))

    def test_get_all_business(self):
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

        # Add business
        res = self.client().post('/api_v1/businesses', json=self.business1)
        self.assertEqual(201, res.status_code)
        self.assertIn('Gracia Afrika', str(res.data))

        # Fetch business
        res = self.client().get('/api_v1/businesses?description=coolest&status=pending')
        self.assertEqual(200, res.status_code)
        self.assertIn('Gracia Afrika', str(res.data))

    def test_business_action_accept(self):
        # Add business
        res = self.client().post('/api_v1/businesses', json=self.business1)
        self.assertEqual(201, res.status_code)
        self.assertIn('Gracia Afrika', str(res.data))

        res = self.client().put('/api_v1/businesses/1/processStatus', json={"status": "accepted"})
        self.assertEqual(200, res.status_code)
        self.assertIn("accepted", str(res.data))

        res = self.client().put('/api_v1/businesses/1/processStatus', json={"status": "refused"})
        self.assertEqual(200, res.status_code)
        self.assertIn("refused", str(res.data))

        res = self.client().put('/api_v1/businesses/1/processStatus', json={"status": "pending"})
        self.assertEqual(200, res.status_code)
        self.assertIn("pending", str(res.data))

        res = self.client().put('/api_v1/businesses/1/processStatus', json={"status": "YOLO"})
        self.assertEqual(400, res.status_code)

        res = self.client().put('/api_v1/businesses/1/processStatus', json={"bad param": "YOLO"})
        self.assertEqual(400, res.status_code)

    def test_business_tag_get(self):
        business = Business(name="business1", category_id="1")
        tag = Tag(name="Tag1")
        tag.addBusinessTag(business)
        category = Category(**self.category1)
        self.setup_minimal_data([business, tag, category])

        res = self.client().get('/api_v1/businesses/1/tags')
        self.assertEqual(200, res.status_code)
        self.assertIn('Tag1', str(res.data))

    def test_business_tag_post(self):
        business = Business(name="business1", category_id="1")
        tag = Tag(name="Tag1")
        tag.addBusinessTag(business)
        category = Category(**self.category1)
        self.setup_minimal_data([business, tag, category])

        res = self.client().post('/api_v1/businesses/1/tags', json=[{ "name": "Beauty"}])
        self.assertEqual(201, res.status_code)
        self.assertIn('Beauty', str(res.data))

    def test_business_tag_post(self):
        business = Business(name="business1", category_id="1")
        tag = Tag(name="Tag1")
        tag.addBusinessTag(business)
        category = Category(**self.category1)
        self.setup_minimal_data([business, tag, category])

        res = self.client().post('/api_v1/businesses/1/tags', json=[{ "name": "Beauty"}])
        self.assertEqual(201, res.status_code)
        self.assertIn('Beauty', str(res.data))

    def test_business_tag_delete(self):
        business = Business(name="business1", category_id="1")
        tag = Tag(name="Tag1")
        tag.addBusinessTag(business)
        category = Category(**self.category1)
        self.setup_minimal_data([business,tag,category])

        res = self.client().delete('/api_v1/businesses/1/tags/1')
        self.assertEqual(204, res.status_code)
