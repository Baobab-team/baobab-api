import csv
from datetime import time

from app.businesses.models import Business, Phone, BusinessHour, Address, SocialLink, Tag


def extract_business_from_csv(file):
    """
    :param file
    :return: array of business
    """
    businesses = []
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            business = Business()

            business.name = row["business_name"]
            business.category_id = row["business_category"]
            business.description = row["business_description"]
            business.slogan = row["business_slogan"]
            business.website = row["business_website"]
            business.notes = row["business_notes"]
            if row["business_email"]:
                business.email = row["business_email"]
            business.capacity = row["business_capacity"] if row["business_capacity"] else 0
            business.payment_types = row["business_payment_types"].split(",")
            hours = extract_business_hours(row["business_hours"])
            business.add_business_hours(hours)
            phones = extract_phones(row["business_phones"])
            business.add_phones(phones)
            addresses = extract_address(row["business_addresses"])
            business.add_addresses(addresses)
            social_links = extract_social_links(row["business_social_links"])
            business.add_social_links(social_links)
            tags = extract_tags(row["business_tags"])
            business.add_tags(tags)
            business.status = Business.StatusEnum.accepted.value

            businesses.append(business)
    return businesses


def extract_business_hours(business_hours_str):
    hours = []
    if business_hours_str:
        days = split_multiple_line_item(business_hours_str)

        for day in days:
            days_spec = day.split("-")
            start_time = [int(t) for t in days_spec[1].split(":")]
            end_time = [int(t) for t in days_spec[2].split(":")]
            hour = BusinessHour(opening_time=time(start_time[0], start_time[1]),
                                closing_time=time(end_time[0], end_time[1]),
                                day=days_spec[0])
            hours.append(hour)
    return hours


def extract_phones(phones_str):
    phones = []
    if phones_str:
        phones_arr = split_multiple_line_item(phones_str)
        for phone in phones_arr:
            parts = phone.split(",")
            phones.append(Phone(extension=parts[0], number=parts[1], type=parts[2]))

    return phones


def extract_address(address_str):
    addresses = []
    if address_str:
        addresses_arr = split_multiple_line_item(address_str)
        for address in addresses_arr:
            parts = address.split(",")
            address = Address()
            address.street_number = parts[0]
            address.street_type = parts[1]
            address.street_name = parts[2]
            address.direction = parts[3]
            address.city = parts[4]
            address.zip_code = parts[5]
            address.region = parts[6]
            address.province = parts[7]
            address.country = parts[8]
            addresses.append(address)

    return addresses


def extract_social_links(social_link_str):
    social_links = []
    if social_link_str:
        social_links_arr = split_multiple_line_item(social_link_str)
        for social_link in social_links_arr:
            parts = social_link.split("-")
            social_link = SocialLink()
            social_link.link = parts[0]
            social_link.type = parts[1]
            social_links.append(social_link)
    return social_links


def extract_tags(tags_str):
    tags = []
    if tags_str:
        tags_arr = split_multiple_line_item(tags_str)
        for tag in tags_arr:
            tags.append(Tag(name=tag))
    return tags


def split_multiple_line_item(str):
    return [item for item in str.replace("\n", "").split(";") if item]
