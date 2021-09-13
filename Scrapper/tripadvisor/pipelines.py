# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import uuid

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
                    name=item["name"],
                    address=item["address"],
                    # unit_price=item["unit_price"],
                    rating=item["rating"],
                    review_count=item["review_count"],
                    description=item["description"],
                    # amenities=item["amenities"]
                )
                # Hotel.create(
                #     id=uuid.uuid4().hex,
                #     name=item["name"],
                #     address=item["address"],
                #     unit_price=item["unit_price"],
                #     rating=item["rating"],
                #     review_count=item["review_count"],
                #     description=item["description"],
                #     amenities=item["amenities"]
                # )

                txn.commit()

            except IntegrityError:
                print("Duplicate Hotel")
                txn.rollback()
