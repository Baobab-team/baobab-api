import json
import unittest

from app import create_app, db
from app.businesses.models import Category, Tag, Business
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
        self.businessA = {
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

        category1 = Category(name="category1")
        category2 = Category(name="category2")
        businessA = Business(name="businessA", category=category1, description="coolest")
        businessB = Business(name="businessB", category=category2)
        businessC = Business(name="businessC", category=category2)
        businessA.process_status(Business.StatusEnum.accepted.value)
        businessB.process_status(Business.StatusEnum.accepted.value)
        businessC.process_status(Business.StatusEnum.refused.value)

        tag1 = Tag(name="Tag1")
        tag2 = Tag(name="Tag2")
        tag1.addBusinessTags([businessA, businessB, businessC])
        tag2.addBusinessTags([businessA])

        # binds the app to the current context
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            for model in [category1, category2, tag1, tag2, businessA, businessB, businessC]:
                db.session.add(model)
            db.session.commit()

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_business_post(self):
        res = self.client().post('/api_v1/businesses',
                                 json={"name": "BusinessA", "category": {"id": 1, "name": "category1"}})
        self.assertIn('BusinessA', str(res.data))
        self.assertEqual(201, res.status_code)

    def test_business_post_add_business_with_existing_category(self):
        res = self.client().post('/api_v1/businesses',
                                 json={"name": "NewBusiness", "category": {"id": 1, "name": "category1"}})
        self.assertIn('NewBusiness', str(res.data))
        self.assertEqual(201, res.status_code)

    def test_business_get_by_id(self):
        res = self.client().get('/api_v1/businesses/2')
        self.assertEqual(200, res.status_code)
        self.assertIn('businessB', str(res.data))

        res = self.client().get('/api_v1/businesses/3')
        self.assertEqual(200, res.status_code)
        self.assertIn('businessC', str(res.data))

        res = self.client().get('/api_v1/businesses/1')
        self.assertEqual(200, res.status_code)
        self.assertIn('businessA', str(res.data))

    def test_business_get(self):
        res = self.client().get('/api_v1/businesses')
        self.assertEqual(200, res.status_code)
        self.assertIn('businessA', str(res.data))
        self.assertIn('businessB', str(res.data))
        self.assertIn('businessC', str(res.data))

    def test_business_update(self):
        res = self.client().put('/api_v1/businesses/1', json={"name": "Pizza hut"})
        self.assertEqual(200, res.status_code)
        self.assertIn('Pizza hut', str(res.data))

    def test_business_get_with_sort_asc(self):
        res = self.client().get('/api_v1/businesses?order_by=name')
        self.assertEqual(200, res.status_code)
        json_data = json.loads(res.data)

        self.assertEqual(3, len(json_data))
        self.assertEqual(json_data[0]["name"], "businessA")
        self.assertEqual(json_data[1]["name"], "businessB")
        self.assertEqual(json_data[2]["name"], "businessC")

    def test_business_get_with_sort_desc(self):
        res = self.client().get('/api_v1/businesses?order_by=name&order=DESC')
        self.assertEqual(200, res.status_code)
        json_data = json.loads(res.data)

        self.assertEqual(3, len(json_data))
        self.assertEqual(json_data[0]["name"], "businessC")
        self.assertEqual(json_data[1]["name"], "businessB")
        self.assertEqual(json_data[2]["name"], "businessA")

    def test_business_get_with_filter_status(self):
        res = self.client().get('/api_v1/businesses?status=accepted')
        self.assertEqual(200, res.status_code)
        self.assertIn('businessA', str(res.data))
        self.assertIn('businessB', str(res.data))
        self.assertNotIn('businessC', str(res.data))

    def test_business_action_accept(self):
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

    def test_business_delete(self):
        res = self.client().delete('/api_v1/businesses/1')
        self.assertEqual(204, res.status_code)
        self.assertEqual("", res.data.decode("utf-8"))

    def test_business_get_after_delete(self):
        res = self.client().delete('/api_v1/businesses/1')
        self.assertEqual(204, res.status_code)
        self.assertEqual("", res.data.decode("utf-8"))

        res = self.client().get('/api_v1/businesses/1')
        self.assertEqual(404, res.status_code)
        self.assertEqual("Business doesnt exist", res.get_json()["message"])

    def test_business_tag_get(self):
        res = self.client().get('/api_v1/businesses/1/tags')
        self.assertEqual(200, res.status_code)
        self.assertIn('Tag1', str(res.data))
        self.assertIn('Tag2', str(res.data))

    def test_business_tag_post(self):
        res = self.client().post('/api_v1/businesses/1/tags', json=[{"name": "Beauty"}])
        self.assertEqual(201, res.status_code)
        self.assertIn('Beauty', str(res.data))

    def test_business_tag_delete(self):
        res = self.client().delete('/api_v1/businesses/1/tags/1')
        self.assertEqual(204, res.status_code)
        self.assertEqual("", res.data.decode("utf-8"))

    def test_business_pagination(self):
        res = self.client().get('/api_v1/businesses?page=1')
        self.assertEqual(200, res.status_code)
        self.assertIn('businessA', str(res.data))
        self.assertIn('businessB', str(res.data))
        self.assertIn('businessC', str(res.data))

    def test_business_pagination_page_1(self):
        res = self.client().get('/api_v1/businesses?page=1&businessPerPage=2')
        self.assertEqual(200, res.status_code)
        self.assertIn('businessA', str(res.data))
        self.assertIn('businessB', str(res.data))
        self.assertNotIn('businessC', str(res.data))

    def test_business_pagination_page_2(self):
        res = self.client().get('/api_v1/businesses?page=2&businessPerPage=2')
        self.assertEqual(200, res.status_code)
        self.assertNotIn('businessA', str(res.data))
        self.assertNotIn('businessB', str(res.data))
        self.assertIn('businessC', str(res.data))

    def test_business_pagination_outside_of_range(self):
        res = self.client().get('/api_v1/businesses?page=100')
        self.assertEqual(200, res.status_code)
        self.assertEqual([], json.loads(res.data))

    def test_autocomplete_search_business(self):
        res = self.client().get('/api_v1/businesses/autocomplete?querySearch=business')
        self.assertEqual(200, res.status_code)
        self.assertEqual(sorted(["businessA","businessB","businessC"]), sorted(json.loads(res.data)))

    def test_autocomplete_search_tag(self):
        res = self.client().get('/api_v1/businesses/autocomplete?querySearch=tag')
        self.assertEqual(200, res.status_code)
        self.assertEqual(sorted(["Tag1","Tag2"]), sorted(json.loads(res.data)))

