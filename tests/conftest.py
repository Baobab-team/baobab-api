import csv
from datetime import time
import pytest

from app import create_app, TestingConfig
from app.businesses.models import *


@pytest.fixture(scope="module")
def test_client():
    app = create_app(config=TestingConfig)
    test_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield test_client
    ctx.pop()


@pytest.fixture(scope="module")
def init_db():
    db.create_all()

    yield db

    db.drop_all()


@pytest.fixture
def business():
    business = Business(name="Business1", website="www.website.com", slogan="Manger bien",
                        description="Restaurant africain vraiment cool",
                        notes="Super notes", capacity=14, email="business@email.com",
                        payment_types=["credit", "debit"], category_id=2,address_raw="123 Kent Est Montreal H0H0H0 Quebec Canada"
                        )
    business.add_business_hour(BusinessHour(opening_time=time(10, 0), closing_time=time(17, 0), day="monday"))
    business.add_business_hour(BusinessHour(opening_time=time(10, 0), closing_time=time(17, 0), day="tuesday"))
    business.add_phone(Phone(number="514-555-5555", extension="+1", type="telephone"))
    business.add_social_link(SocialLink(type="instagram", link="www.nn.com"))

    return business


@pytest.fixture
def business_upload_file(tmp_path):
    rows = [
        ["business_category","business_name", "business_description", "business_slogan", "business_website", "business_email",
         "business_status", "business_notes", "business_capacity", "business_payment_types", "business_hours",
         "business_phones", "business_addresses", "business_social_links", "business_tags"],
        [1, "Business1", "Restaurant africain vraiment cool", "Manger bien", "www.website.com",
         "business@email.com", "", "Super notes", "14", "credit,debit", "monday-10:00-17:00;tuesday-10:00-17:00;",
         "+1,514-555-5555,telephone;", "123 Kent Est Montreal H0H0H0 Quebec Canada",
         "www.nn.com-Instagram;", "Haitian;African"]
    ]
    upload_folder = tmp_path / "uploads"
    upload_folder.mkdir()
    file = upload_folder / "file.csv"
    with open(file, 'w') as csvfile:
        writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)
        for line in rows:
            writer.writerow(line)
    return file

