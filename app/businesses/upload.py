import csv
from datetime import time

from app.businesses.models import Business, Phone, BusinessHour


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
            if row["business_hours"]:
                days = [day for day in row["business_hours"].replace("\n", "").split(";") if day]

                for day in days:
                    days_spec = day.split("-")
                    start_time = [int(t) for t in days_spec[1].split(":")]
                    end_time = [int(t) for t in days_spec[2].split(":")]
                    hour = BusinessHour(opening_time=time(start_time[0], start_time[1]),
                                        closing_time=time(end_time[0], end_time[1]),
                                        day=days_spec[0])
                    business.add_business_hour(hour)

            if row["business_phones"]:
                phones_arr = [phone for phone in row["business_phones"].replace("\n", "").split(";") if phone]
                for phone in phones_arr:
                    parts = phone.split("--")
                    business.add_phone(Phone(extension=parts[0], number=parts[1], type=parts[2]))

    return business


def validate_column():
    pass
