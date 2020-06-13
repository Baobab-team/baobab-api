import csv
from datetime import time

from app.businesses.models import Business, Phone, BusinessHour, Address


def extract_business_from_csv(file):
    business = Business()
    with open(file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:

            business.name = row["business_name"]
            business.description = row["business_description"]
            business.slogan = row["business_slogan"]
            business.website = row["business_website"]
            business.notes = row["business_notes"]
            business.email = row["business_email"]
            business.capacity = row["business_capacity"]
            business.payment_types = row["business_payment_types"].split(",")

            hours = extract_business_hours(row["business_hours"])
            business.add_business_hours(hours)
            phones = extract_phones(row["business_phones"])
            business.add_phones(phones)
            addresses = extract_address(row["business_addresses"])
            business.add_addresses(addresses)

    return business


def extract_business_hours(business_hours_str):
    hours = []
    if business_hours_str:
        days = [day for day in business_hours_str.replace("\n", "").split(";") if day]

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
        phones_arr = [phone for phone in phones_str.replace("\n", "").split(";") if phone]
        for phone in phones_arr:
            parts = phone.split("--")
            phones.append(Phone(extension=parts[0], number=parts[1], type=parts[2]))

    return phones


def extract_address(address_str):
    addresses = []
    if address_str:
        addresses_arr = [phone for phone in address_str.replace("\n", "").split(";") if phone]
        for address in addresses_arr:
            parts = address.split("--")
            # assert len(parts) == 9
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
