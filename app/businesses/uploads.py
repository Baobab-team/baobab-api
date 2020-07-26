import csv
import os
from datetime import time

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from app.businesses.models import Business, Phone, BusinessHour, Address, SocialLink, Tag, BusinessUpload, Category
from app.businesses.repositories import BusinessUploadRepository, TagRepository, CategoryRepository

upload_repository = BusinessUploadRepository()
tag_repository = TagRepository()
category_repository = CategoryRepository()


def process_file(filename):
    upload = BusinessUpload()
    upload.filename = filename
    try:
        if os.stat(filename).st_size == 0:
            raise Exception("File is empty")
        upload.businesses = extract_business_from_csv(filename)
        upload.success = True
        upload_repository.save(upload)
    except (Exception, SQLAlchemyError) as e:
        current_app.logger.error(str(e.args[0]))
        upload.businesses = []
        upload.success = False
        upload.error_message = str(e.args[0])
        upload_repository.save(upload)

    return upload


def extract_business_from_csv(file):
    """
    :param file
    :return: array of business
    """
    businesses = []
    with open(file, mode='r') as csv_file:
        try:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data = get_business_data(row)
                businesses.append(Business(**data))
            if len(businesses) == 0:
                raise Exception("No businesses in the file")
            return businesses
        except Exception as e:
            current_app.logger.error(str(e))
            raise


def get_business_data(row):
    data = {
        "category": extract_category(row["business_category"]),
        "name": row["business_name"],
        "category_id": row["business_category"],
        "description": row["business_description"],
        "addresses": extract_address(row["business_addresses"]),
        "business_hours": extract_business_hours(row["business_hours"]),
        "phones": extract_phones(row["business_phones"]),
        "slogan": row["business_slogan"],
        "website": row["business_website"],
        "tags": extract_tags(row["business_tags"]),
        "payment_types": row["business_payment_types"].split(","),
        "social_links": extract_social_links(row["business_social_links"]),
        "status": Business.StatusEnum.accepted.value,
        "capacity": row["business_capacity"] if row["business_capacity"] else 0,
        "notes": row["business_notes"]
    }
    if row["business_email"]:
        data["email"] = row["business_email"]
    return data


def extract_category(category_name):
    category = category_repository.filter(**{"name": category_name}).one_or_none()
    if category is None:
        category = Category(name=category_name.lower())
        category_repository.save(category)
    return category


def extract_business_hours(business_hours_str):
    hours = []
    if business_hours_str:
        days = split_multiple_line_item(business_hours_str)

        for day in days:
            days_spec = day.split("-")
            if len(days_spec) != 3:
                raise Exception(f"Invalid business hours: {' '.join(days_spec)}")
            start_time = [int(t) for t in days_spec[1].split(":")]
            end_time = [int(t) for t in days_spec[2].split(":")]
            if len(start_time) != 2:
                raise Exception(f"Invalid business hours: f{start_time}")
            if len(end_time) != 2:
                raise Exception(f"Invalid business hours: f{end_time}")
            hour = BusinessHour(opening_time=time(start_time[0], start_time[1]),
                                closing_time=time(end_time[0], end_time[1]),
                                day=days_spec[0].lower())
            hours.append(hour)
    return hours


def extract_phones(phones_str):
    phones = []
    if phones_str:
        phones_arr = split_multiple_line_item(phones_str)
        for phone in phones_arr:
            parts = phone.split(",")
            if len(parts) != 3:
                raise Exception(F"Invalid phone: {' '.join(parts)}")
            phones.append(Phone(extension=parts[0], number=parts[1], type=parts[2]))

    return phones


def extract_address(address_str):
    addresses = []
    if address_str:
        addresses_arr = split_multiple_line_item(address_str)
        for address in addresses_arr:
            arr = address.split(",")
            if len(arr) != 9:
                raise Exception("Invalid address: {}", ' '.join(arr))
            data = get_address_data(arr)
            addresses.append(Address(**data))

    return addresses


def get_address_data(arr):
    return {
        "street_number": arr[0],
        "street_type": arr[1],
        "street_name": arr[2],
        "direction": arr[3],
        "city": arr[4],
        "zip_code": arr[5],
        "region": arr[6],
        "province": arr[7],
        "country": arr[8]
    }


def extract_social_links(social_link_str):
    social_links = []
    if social_link_str:
        social_links_arr = split_multiple_line_item(social_link_str)

        for social_link in social_links_arr:
            parts = social_link.split("-")
            if len(parts) != 2:
                raise Exception("Invalid Social link: {}".format(' '.join(parts)))
            social_link = SocialLink()
            social_link.link = parts[0].lower()
            social_link.type = parts[1].lower()
            social_links.append(social_link)
    return social_links


def extract_tags(tags_str):
    tags = []
    if tags_str:
        tags_arr = split_multiple_line_item(tags_str)
        for tag in tags_arr:
            tags.append(Tag(name=tag.lower()))
    tags = tag_repository.get_tags_with_id(tags)
    return tags


def split_multiple_line_item(str):
    return [item for item in str.replace("\n", "").split(";") if item]
