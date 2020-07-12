import json


def test_post(test_client, db_session):
    res = test_client.post('/api_v1/tags', json={"name": "haiti"})
    json_data = json.loads(res.data)
    assert 201 == res.status_code
    assert "haiti" == json_data.get("name")


def test_put(test_client, tag1):
    res = test_client.put('/api_v1/tags/1', json={"name": "perle des caraibes"})
    json_data = json.loads(res.data)
    assert 200 == res.status_code
    assert "perle des caraibes" == json_data.get("name")


def test_get_collection(test_client, tag1, tag2):
    res = test_client.get('/api_v1/tags')
    json_data = json.loads(res.data)
    assert 200 == res.status_code
    assert 2 == len(json_data)
    assert "tag1" == json_data[0].get("name")
    assert "tag2" == json_data[1].get("name")


def test_get_scalar(test_client, tag2):
    res = test_client.get('/api_v1/tags/2')
    json_data = json.loads(res.data)
    assert 200 == res.status_code
    assert "tag2" == json_data.get("name")


def test_delete(test_client,tag1):
    res = test_client.delete('/api_v1/tags/1')
    assert 204 == res.status_code
    assert "" == res.data.decode("utf-8")
