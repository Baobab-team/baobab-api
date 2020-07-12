import json

import pytest

from app.businesses.models import Category


def test_get_scalar(test_client, db_session, category1):
    res = test_client.get('/api_v1/categories/1')
    json_data = json.loads(res.data)
    assert res.status_code, 200
    assert 'category1' == json_data.get("name")


def test_get_collection(test_client, db_session, category1, category2):
    res = test_client.get('/api_v1/categories')
    json_data = json.loads(res.data)
    assert res.status_code, 200
    assert len(json_data) == 2
    assert 'category1' == json_data[0].get("name")
    assert 'category2' == json_data[1].get("name")


def test_post(test_client, db_session):
    res = test_client.post('/api_v1/categories', json={"name": "category1"})
    json_data = json.loads(res.data)
    assert res.status_code == 201
    assert 'category1' == json_data.get("name")


def test_put(test_client, db_session, category1):
    res = test_client.put('/api_v1/categories/1', json={'name': 'new name'})
    json_data = json.loads(res.data)
    assert 200 == res.status_code
    assert "new name" == json_data.get("name")


def test_delete(test_client, category1):
    res = test_client.delete('/api_v1/categories/1')
    assert 204 == res.status_code


def test_invalid_delete(test_client):
    res = test_client.delete('/api_v1/categories/10')
    assert 404 == res.status_code
