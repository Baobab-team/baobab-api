from app.businesses.extract import extract_business_from_csv


def test_extract_business_from_csv(test_app,business, business_upload_file):
    businesses = extract_business_from_csv(business_upload_file)
    assert businesses[0] == business
