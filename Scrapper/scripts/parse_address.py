import json
import os
import sys

sys.path.append(os.getcwd())

import dotenv
import googlemaps
import peewee
import tqdm

from playhouse import migrate

from tripadvisor.database.schema import Hotel
from tripadvisor.database.schema import database


def get_address_component(geocode_data, query_strings):

    query_result = None

    for result in geocode_data:

        address_components = result["address_components"]

        for address_component in address_components:

            if query_strings[0] in address_component["types"] or query_strings[-1] in address_component["types"]:
                query_result = address_component["long_name"]

        if query_result:
            return query_result
        else:

            for address_component in address_components:

                if "administrative_area_level_3" in address_component["types"]:
                    query_result = address_component["long_name"]

        if query_result:
            return query_result
        else:

            for address_component in address_components:

                if "administrative_area_level_3" in address_component["types"]:
                    return address_component["long_name"]


def migrate_database():

    try:
        migrator = migrate.SqliteMigrator(database)
        city_field = peewee.TextField(
            null=True,
            verbose_name="Hotel City",
        )

        country_field = peewee.TextField(
            null=True,
            verbose_name="Hotel Country",
        )

        with database.atomic():

            migrate.migrate(
                migrator.add_column("hotel", "city", city_field),
                migrator.add_column("hotel", "country", country_field)
            )

    except peewee.OperationalError as error:
        # print("Error")
        pass

if __name__ == "__main__":

    migrate_database()
    dotenv.load_dotenv()
    gmaps = googlemaps.Client(key=os.environ.get("GOOGLE_GEOCODE_API_KEY"))

    for hotel in tqdm.tqdm(Hotel.select()):

        if hotel.city is None or hotel.country is None:
            geocode_data = gmaps.geocode(hotel.address)

            city = get_address_component(
                geocode_data, ["locality", "postal_town"])
            country = get_address_component(geocode_data, ["country"])

            with database.atomic():

                hotel.city = city
                hotel.country = country

                hotel.save()
