# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import random
import uuid

import lorem


from itemadapter import ItemAdapter
from peewee import IntegrityError

from tripadvisor.database import create_data

from tripadvisor.database.schema import database
from tripadvisor.database.schema import Hotel


class TripadvisorPipeline:

    def __init__(self):
        super().__init__()

        create_data.setup_database()

    def process_item(self, item, spider):

        with database.atomic() as txn:

            try:
                Hotel.create(
                    id=uuid.uuid4().hex,
                    hotel_id=item["hotel_id"],
                    name=item["name"],
                    address=item["address"],
                    unit_price=item["unit_price"],
                    rating=item["rating"],
                    review_count=item["review_count"],
                    description=item["description"],
                    # amenities=item["amenities"]
                )

                txn.commit()

            except IntegrityError:
                txn.rollback()

            except:
                pass


class DefaultItemsPipeline:
    """Populates some fields with some random values if the Scrapper couldn't scrape them"""

    def process_item(self, item, spider):

        try:
            unit_price = item["unit_price"]

        except KeyError:

            item["unit_price"] = random.randint(75, 125)

        try:
            description = item["description"]

        except KeyError:

            item["description"] = lorem.paragraph()

        try:
            rating = item["rating"]

        except KeyError:

            item["rating"] = round(random.uniform(3, 5), 2)

        try:
            review_count = item["review_count"]

        except KeyError:

            item["review_count"] = random.randint(1, 128)


        return item
