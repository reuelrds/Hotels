import json
import re


def process_description(text):
    description_dict = json.loads(text)
    return description_dict["load"][-1]["locationDescription"]


def process_amenities(text):
    amenities_dict = json.loads(text)
    amenities = amenities_dict["load"][-1]["amenities"]

    amenities.pop("nonHighlightedAmenities")

    return amenities


def strip_currency_symbol(text):
    return re.sub(r"[$]", '', text)


def get_review_count(text):
    return text.split()[0]


def to_int(text):
    return int(text)


def to_float(text):
    return float(text)
