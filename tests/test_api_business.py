import json


def test_business_post(test_client):
    res = test_client.post('/api_v1/businesses',
                           json={"name": "BusinessA", "category": {"id": 1, "name": "category1"}})
    json_data = json.loads(res.data)
    assert 201 == res.status_code
    assert json_data.get("name") == 'BusinessA'

    # TODO REMOVE . Reminder to add models tests
    # def test_business_post_add_business_with_existing_category(self):
    #     res = self.client().post('/api_v1/businesses',
    #                              json={"name": "NewBusiness", "category": {"id": 1, "name": "category1"}})
    #     self.assertIn('NewBusiness', str(res.data))
    #     self.assertEqual(201, res.status_code)
    #


def test_get_scalar(test_client, business1):
    res = test_client.get('/api_v1/businesses/1')
    json_data = json.loads(res.data)
    assert 200 == res.status_code
    assert 'business1' == json_data.get("name")


def test_get_collection(test_client, business1):
    res = test_client.get('/api_v1/businesses')
    json_data = json.loads(res.data)
    assert 200 == res.status_code
    assert 1 == len(json_data)
    assert 'business1' == json_data[0].get("name")

    #


def test_update(test_client, business1):
    res = test_client.put('/api_v1/businesses/1', json={"name": "Pizza hut"})
    json_data = json.loads(res.data)
    assert 200, res.status_code
    assert 'Pizza hut' == json_data.get("name")

    # TODO Remove
    # def test_business_get_with_sort_asc(self):
    #     res = self.client().get('/api_v1/businesses?order_by=name')
    #     self.assertEqual(200, res.status_code)
    #     json_data = json.loads(res.data)
    #
    #     self.assertEqual(3, len(json_data))
    #     self.assertEqual(json_data[0]["name"], "businessA")
    #     self.assertEqual(json_data[1]["name"], "businessB")
    #     self.assertEqual(json_data[2]["name"], "businessC")
    #
    # def test_business_get_with_sort_desc(self):
    #     res = self.client().get('/api_v1/businesses?order_by=name&order=DESC')
    #     self.assertEqual(200, res.status_code)
    #     json_data = json.loads(res.data)
    #
    #     self.assertEqual(3, len(json_data))
    #     self.assertEqual(json_data[0]["name"], "businessC")
    #     self.assertEqual(json_data[1]["name"], "businessB")
    #     self.assertEqual(json_data[2]["name"], "businessA")
    #
    # def test_business_get_with_filter_status(self):
    #     res = self.client().get('/api_v1/businesses?status=accepted')
    #     self.assertEqual(200, res.status_code)
    #     self.assertIn('businessA', str(res.data))
    #     self.assertIn('businessB', str(res.data))
    #     self.assertNotIn('businessC', str(res.data))
    #

    # def test_business_action_accept(self):
    #     res = self.client().put('/api_v1/businesses/1/processStatus', json={"status": "accepted"})
    #     self.assertEqual(200, res.status_code)
    #     self.assertIn("accepted", str(res.data))
    #
    #     res = self.client().put('/api_v1/businesses/1/processStatus', json={"status": "refused"})
    #     self.assertEqual(200, res.status_code)
    #     self.assertIn("refused", str(res.data))
    #
    #     res = self.client().put('/api_v1/businesses/1/processStatus', json={"status": "pending"})
    #     self.assertEqual(200, res.status_code)
    #     self.assertIn("pending", str(res.data))
    #
    #     res = self.client().put('/api_v1/businesses/1/processStatus', json={"status": "YOLO"})
    #     self.assertEqual(400, res.status_code)
    #
    #     res = self.client().put('/api_v1/businesses/1/processStatus', json={"bad param": "YOLO"})
    #     self.assertEqual(400, res.status_code)
    #
    # def test_business_delete(self):
    #     res = self.client().delete('/api_v1/businesses/1')
    #     self.assertEqual(204, res.status_code)
    #     self.assertEqual("", res.data.decode("utf-8"))


    # def test_business_tag_get(self):
    #     res = self.client().get('/api_v1/businesses/1/tags')
    #     self.assertEqual(200, res.status_code)
    #     self.assertIn('Tag1', str(res.data))
    #     self.assertIn('Tag2', str(res.data))
    #
    # def test_business_tag_post(self):
    #     res = self.client().post('/api_v1/businesses/1/tags', json=[{"name": "Beauty"}])
    #     self.assertEqual(201, res.status_code)
    #     self.assertIn('Beauty', str(res.data))
    #
    # def test_business_tag_delete(self):
    #     res = self.client().delete('/api_v1/businesses/1/tags/1')
    #     self.assertEqual(204, res.status_code)
    #     self.assertEqual("", res.data.decode("utf-8"))
    #
    # def test_business_pagination(self):
    #     res = self.client().get('/api_v1/businesses?page=1')
    #     self.assertEqual(200, res.status_code)
    #     self.assertIn('businessA', str(res.data))
    #     self.assertIn('businessB', str(res.data))
    #     self.assertIn('businessC', str(res.data))
    #
    # def test_business_pagination_page_1(self):
    #     res = self.client().get('/api_v1/businesses?page=1&businessPerPage=2')
    #     self.assertEqual(200, res.status_code)
    #     self.assertIn('businessA', str(res.data))
    #     self.assertIn('businessB', str(res.data))
    #     self.assertNotIn('businessC', str(res.data))
    #
    # def test_business_pagination_page_2(self):
    #     res = self.client().get('/api_v1/businesses?page=2&businessPerPage=2')
    #     self.assertEqual(200, res.status_code)
    #     self.assertNotIn('businessA', str(res.data))
    #     self.assertNotIn('businessB', str(res.data))
    #     self.assertIn('businessC', str(res.data))
    #
    # def test_business_pagination_outside_of_range(self):
    #     res = self.client().get('/api_v1/businesses?page=100')
    #     self.assertEqual(200, res.status_code)
    #     self.assertEqual([], json.loads(res.data))
    #
    # def test_autocomplete_search_business(self):
    #     res = self.client().get('/api_v1/businesses/autocomplete?querySearch=buzines')
    #     self.assertEqual(200, res.status_code)
    #     self.assertEqual(sorted(["businessA", "businessB", "businessC"]), sorted(json.loads(res.data)))
    #
    # def test_autocomplete_search_tag(self):
    #     res = self.client().get('/api_v1/businesses/autocomplete?querySearch=tag')
    #     self.assertEqual(200, res.status_code)
    #     self.assertEqual(sorted(["Tag1", "Tag2"]), sorted(json.loads(res.data)))
    #
    # def test_autocomplete_search_no_query_search(self):
    #     res = self.client().get('/api_v1/businesses/autocomplete')
    #     self.assertEqual(400, res.status_code)
    #     self.assertEqual("Missing query search parameter", json.loads(res.data)["message"])
