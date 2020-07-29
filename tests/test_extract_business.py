from app.businesses.data import extract_business_from_csv


def test_extract_business_from_csv(test_client, init_db, business, business_upload_file):
    businesses = extract_business_from_csv(business_upload_file)
    assert businesses[0] == business
