import csv
import json
import os
import shutil
import unittest

from werkzeug.datastructures import FileStorage

from app import create_app, db
from app.businesses.models import Category, Tag, Business
from app.config import TestingConfig

BUSINESSES_FILE_UPLOADED_CSV = os.path.join(os.path.dirname(__file__), "businesses_upload.csv")


class BusinessTestCase(unittest.TestCase):
    """This class represents the business test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config=TestingConfig)
        self.app.config["UPLOAD_FOLDER"] = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads_for_test'))
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
        businessA.add_tags([tag2, tag1])
        businessB.add_tag(tag1)
        businessC.add_tag(tag1)

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
        folder = self.app.config["UPLOAD_FOLDER"]
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        if os.path.exists(BUSINESSES_FILE_UPLOADED_CSV):
            os.remove(BUSINESSES_FILE_UPLOADED_CSV)


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
        res = self.client().get('/api_v1/businesses/autocomplete?querySearch=buzines')
        self.assertEqual(200, res.status_code)
        self.assertEqual(sorted(["businessA","businessB","businessC"]), sorted(json.loads(res.data)))

    def test_autocomplete_search_tag(self):
        res = self.client().get('/api_v1/businesses/autocomplete?querySearch=tag')
        self.assertEqual(200, res.status_code)
        self.assertEqual(sorted(["Tag1","Tag2"]), sorted(json.loads(res.data)))

    def test_autocomplete_search_no_query_search(self):
        res = self.client().get('/api_v1/businesses/autocomplete')
        self.assertEqual(400, res.status_code)
        self.assertEqual("Missing query search parameter", json.loads(res.data)["message"])

    def test_business_upload_csv(self):
        rows = [
            ["business_category", "business_name", "business_description", "business_slogan", "business_website",
             "business_email",
             "business_status", "business_notes", "business_capacity", "business_payment_types", "business_hours",
             "business_phones", "business_addresses", "business_social_links", "business_tags"],
            [1, "Gracia Afrika", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            [1, "restaurant akwaba", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        ]
        with open(BUSINESSES_FILE_UPLOADED_CSV, 'w') as csvfile:
            writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)
            for line in rows:
                writer.writerow(line)
        my_file = FileStorage(
            stream=open(BUSINESSES_FILE_UPLOADED_CSV, "rb"),
            filename="businesses_file_upload.csv",
            content_type="text/csv",
        ),
        data = {'file': my_file}
        res = self.client().post(
            '/api_v1/businesses/upload', data=data, content_type='multipart/form-data',
        )
        self.assertEqual(200, res.status_code)
        jsondata = json.loads(res.data)
        self.assertEqual(True, jsondata.get("success"))
        self.assertEqual(2, jsondata.get("businesses_count"))
        self.assertIsNotNone(jsondata.get("filename"))
        self.assertIsNotNone(jsondata.get("created_at"))
        self.assertIsNone(jsondata.get("deleted_at"))
        self.assertEqual("Gracia Afrika", jsondata.get("businesses")[0].get("name"))
        self.assertEqual("restaurant akwaba", jsondata.get("businesses")[1].get("name"))

    def test_business_upload_csv_duplicate_name(self):
        rows = [
            ["business_category", "business_name", "business_description", "business_slogan", "business_website",
             "business_email",
             "business_status", "business_notes", "business_capacity", "business_payment_types", "business_hours",
             "business_phones", "business_addresses", "business_social_links", "business_tags"],
            [1, "Gracia Afrika", "", "", "", "", "", "", "", "", "", "", "", "", ""],
            [1, "Gracia Afrika", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        ]
        with open(BUSINESSES_FILE_UPLOADED_CSV, 'w') as csvfile:
            writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)
            for line in rows:
                writer.writerow(line)
        my_file = FileStorage(
            stream=open(BUSINESSES_FILE_UPLOADED_CSV, "rb"),
            filename="businesses_file_upload.csv",
            content_type="text/csv",
        ),
        data = {'file': my_file}
        res = self.client().post(
            '/api_v1/businesses/upload', data=data, content_type='multipart/form-data',
        )
        self.assertEqual(200, res.status_code)
        jsondata = json.loads(res.data)
        self.assertEqual(False, jsondata.get("success"))
        self.assertEqual(0, jsondata.get("businesses_count"))
        self.assertIsNotNone(jsondata.get("filename"))
        self.assertIsNotNone(jsondata.get("error_message"))
        self.assertIsNotNone(jsondata.get("created_at"))
        self.assertIsNone(jsondata.get("deleted_at"))
