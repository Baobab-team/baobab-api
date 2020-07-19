from app.businesses.uploads import extract_business_from_csv
from app.businesses.models import Tag
import mock

@mock.patch('app.businesses.uploads.tag_repository.get_tags_with_id', return_value=[Tag(name="Haitian"), Tag(name="African")])
def test_extract_business_from_csv(test_app,business, business_upload_file):
    businesses = extract_business_from_csv(business_upload_file)
    assert businesses[0] == business
