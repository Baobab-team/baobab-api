import csv
from datetime import time
from functools import partial

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app import create_app
from app.businesses.models import *
from app.config import TestingConfig


@pytest.fixture
def test_config(tmpdir):
    return {
        "UPLOAD_FOLDER": tmpdir.mkdir("uploads")
    }


@pytest.fixture
def test_app(db_session, test_config):
    app = create_app(config=TestingConfig)
    setattr(app, 'session', db_session)
    app.config.update(test_config)
    return app


@pytest.fixture
def test_client(test_app):
    with test_app.test_client() as client:
        yield client


@pytest.yield_fixture
def app_context(test_app):
    with test_app.app_context() as context:
        yield context


@pytest.fixture
def db_engine():
    engine = create_engine('sqlite://')
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def factory(db_session):
    return partial(make_obj, db_session)


def make_obj(session, entity, **kwargs):
    obj = entity(**kwargs)
    session.add(obj)
    session.flush()
    return obj


@pytest.fixture
def db_session(db_engine):
    return scoped_session(
        sessionmaker(bind=db_engine, autocommit=False, autoflush=True)
    )


@pytest.fixture
def category1(factory):
    return factory(
        Category,
        name="category1",
        id=1
    )


@pytest.fixture
def category2(factory):
    return factory(
        Category,
        name="category2",
        id=2
    )

@pytest.fixture
def tag1(factory):
    return factory(
        Tag,
        name="tag1",
        id=1
    )

@pytest.fixture
def tag2(factory):
    return factory(
        Tag,
        name="tag2",
        id=2
    )


@pytest.fixture
def business_upload1(factory, category1):
    return factory(
        BusinessUpload,
        error_message="",
        filename="file1.csv",
        success=True,
        businesses=[Business(category_id=1, name="business1")]
    )

@pytest.fixture
def business():
    business = Business(name="Business1", website="www.website.com", slogan="Manger bien",
                        description="Restaurant africain vraiment cool",
                        notes="Super notes", capacity=14, email="business@email.com",
                        payment_types=["credit", "debit"],category_id=1
                        )
    business.add_business_hour(BusinessHour(opening_time=time(10, 0), closing_time=time(17, 0), day="monday"))
    business.add_business_hour(BusinessHour(opening_time=time(10, 0), closing_time=time(17, 0), day="tuesday"))
    business.add_phone(Phone(number="514-555-5555", extension="+1", type="telephone"))
    business.add_address(
        Address(street_number="123", street_type="street", street_name="Kent", zip_code="H0H0H0", country="Canada",
                direction="Est", region="REGION", city="Montreal", province="Quebec"))
    business.add_social_link(SocialLink(type="Instagram", link="www.nn.com"))
    business.add_tags([Tag(name="Haitian"), Tag(name="African")])

    return business


@pytest.fixture
def business_upload_file(tmp_path):
    rows = [
        ["business_category","business_name", "business_description", "business_slogan", "business_website", "business_email",
         "business_status", "business_notes", "business_capacity", "business_payment_types", "business_hours",
         "business_phones", "business_addresses", "business_social_links", "business_tags"],
        [1,"Business1", "Restaurant africain vraiment cool", "Manger bien", "www.website.com",
         "business@email.com", "", "Super notes", "14", "credit,debit", "monday-10:00-17:00;tuesday-10:00-17:00;",
         "+1,514-555-5555,telephone;", "123,street,Kent,Est,Montreal,H0H0H0,REGION,Quebec,Canada;",
         "www.nn.com-Instagram;", "Haitian;African"]
    ]
    d = tmp_path / "dir"
    d.mkdir()
    business_upload_file = d / "businesses_file_upload.csv"
    with open(business_upload_file, 'w') as csvfile:
        writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)
        for line in rows:
            writer.writerow(line)
    return business_upload_file


@pytest.fixture
def business_upload_file_with_duplicate(tmp_path):
    rows = [
        ["business_category", "business_name", "business_description", "business_slogan", "business_website",
         "business_email",
         "business_status", "business_notes", "business_capacity", "business_payment_types", "business_hours",
         "business_phones", "business_addresses", "business_social_links", "business_tags"],
        [1, "Gracia Afrika", "", "", "", "", "", "", "", "", "", "", "", "", ""],
        [1, "Gracia Afrika", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    ]
    d = tmp_path / "dir"
    d.mkdir()
    business_upload_file = d / "businesses_file_upload.csv"
    with open(business_upload_file, 'w') as csvfile:
        writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)
        for line in rows:
            writer.writerow(line)
    return business_upload_file
