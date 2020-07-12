import json
from werkzeug.datastructures import FileStorage


def test_business_upload_csv(test_client, business_upload_file):

    my_file = FileStorage(
        stream=open(business_upload_file, "rb"),
        filename="businesses_file_upload.csv",
        content_type="text/csv",
    ),
    data = {'file': my_file}
    res = test_client.post(
        '/api_v1/businesses/uploads', data=data, content_type='multipart/form-data',
    )
    assert  res.status_code == 200
    jsondata = json.loads(res.data)
    assert True, jsondata.get("success")
    assert jsondata.get("businesses_count") == 1
    assert jsondata.get("filename") is not None
    assert jsondata.get("created_at") is not None
    assert jsondata.get("deleted_at") is None
    assert jsondata.get("businesses")[0].get("name") == "Business1"



def test_business_upload_csv_duplicate_name(test_client, business_upload_file_with_duplicate):
    my_file = FileStorage(
        stream=open(business_upload_file_with_duplicate, "rb"),
        filename="businesses_file_upload.csv",
        content_type="text/csv",
    ),
    data = {'file': my_file}
    res = test_client.post(
        '/api_v1/businesses/uploads', data=data, content_type='multipart/form-data',
    )
    assert 200, res.status_code
    json_data = json.loads(res.data)
    assert not json_data.get("success")
    assert 0 == json_data.get("businesses_count")
    assert json_data.get("filename") is not None
    assert json_data.get("error_message") is not None
    assert json_data.get("created_at") is not None
    assert json_data.get("deleted_at") is None


def test_business_upload_get_scalar(test_client, business_upload1):
    res = test_client.get('/api_v1/businesses/uploads/1')
    json_data = json.loads(res.data)
    assert 200 == res.status_code
    assert 1 == json_data.get("businesses_count")
    assert json_data.get("success")
    assert "file1.csv" == json_data.get("filename")


def test_business_upload_get_collection(test_client, business_upload1):
    res = test_client.get('/api_v1/businesses/uploads')
    json_data = json.loads(res.data)
    assert 200 == res.status_code
    assert 1 == len(json_data)
    assert 1 == json_data[0].get("businesses_count")
    assert json_data[0].get("success")
    assert "file1.csv" == json_data[0].get("filename")
