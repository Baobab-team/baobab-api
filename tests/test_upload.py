import os
from datetime import time

from app.businesses.models import Business, Phone, BusinessHour
from app.businesses.upload import extract_business_from_csv

BUSINESSES_CSV = os.path.join(os.path.dirname(__file__), 'businesses.csv')


def test_extract_business_from_csv():
    business = extract_business_from_csv(BUSINESSES_CSV)
    expected_business = Business(name="Gracia Afrika", website="www.website.com", slogan="Manger bien",
                                 description="Restaurant africain vraiment cool",
                                 notes="Super notes", capacity=14, email="business@email.com",
                                 payment_types=["credit", "debit"],
                                 )
    expected_business.add_business_hour(BusinessHour(opening_time=time(10, 0), closing_time=time(17, 0), day="monday"))
    expected_business.add_business_hour(BusinessHour(opening_time=time(10, 0), closing_time=time(17, 0), day="tuesday"))
    expected_business.add_phone(Phone(number="514-555-5555", extension="+1", type="telephone"))
    assert business == expected_business
