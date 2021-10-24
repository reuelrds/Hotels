# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import json
import scrapy

from itemloaders.processors import MapCompose, TakeFirst
from tripadvisor.utils import preprocessers


class HotelItem(scrapy.Item):

    name = scrapy.Field(
        output_processor=TakeFirst()
    )
    address = scrapy.Field(
        output_processor=TakeFirst()
    )
    unit_price = scrapy.Field(
        input_processor=MapCompose(
            preprocessers.strip_currency_symbol,
            preprocessers.to_int,
        ),
        output_processor=TakeFirst()
    )
    rating = scrapy.Field(
        input_processor=MapCompose(preprocessers.to_float),
        output_processor=TakeFirst()
    )
    review_count = scrapy.Field(
        input_processor=MapCompose(
            preprocessers.get_review_count,
            preprocessers.to_int,
        ),
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        input_processor=MapCompose(preprocessers.process_description),
        output_processor=TakeFirst()
    )

    hotel_id = scrapy.Field(
        output_processor=TakeFirst()
    )
    # amenities = scrapy.Field(
    #     input_processor=MapCompose(preprocessers.process_amenities),
    #     output_processor=TakeFirst()
    # )
