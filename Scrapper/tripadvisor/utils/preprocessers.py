import json
import re

import lorem


def process_description(text):

    if text[0] == "{":
        try:
            description_dict = json.loads(text)
            return description_dict["load"][-1]["locationDescription"]
        except:

            try:
                return description_dict["load"][-1]["partnerDescription"]["description"]
            except:
                return lorem.paragraph()
    else:
        return lorem.paragraph()


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
    try:
        return int(text)
    except:
        return


def to_float(text):
    return float(text)
