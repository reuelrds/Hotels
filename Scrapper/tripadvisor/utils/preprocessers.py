import json


def process_description(text_list):
    description_dict = json.loads(text_list[0])
    return description_dict["load"][-1]["locationDescription"]


def process_amenities(text_list):
    amenities_dict = json.loads(text_list[0])
    amenities = amenities_dict["load"][-1]["amenities"]

    print(f"AMENITIE: {amenities.keys()}")

    amenities.pop("nonHighlightedAmenities")

    return amenities
