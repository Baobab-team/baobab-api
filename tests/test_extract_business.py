import os

from app.businesses.extract import extract_business_from_csv

BUSINESSES_CSV = os.path.join(os.path.dirname(__file__), 'businesses_file_upload.csv')


def test_extract_business_from_csv(business, business_upload_file):
    businesses = extract_business_from_csv(BUSINESSES_CSV)

    assert businesses[0] == business