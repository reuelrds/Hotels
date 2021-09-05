import scrapy
from scrapy.loader import ItemLoader

from tripadvisor.items import HotelItem


class HotelsSpider(scrapy.Spider):
    name = "hotels"

    start_urls = ['http://localhost:8080/index.html']

    def __init__(self):
        super().__init__()

    def parse(self, response, **kwargs):
        self.logger.info("First Spider working")

        loader = ItemLoader(item=HotelItem(), response=response)

        loader.add_css("rating", '.bvcwU.P::text')
        loader.add_css("unit_price", '.cGGHC.Wi.Wa::text')
        loader.add_css("review_count", '.btQSs.q.Wi.z.Wc::text')

        loader.add_xpath(
            "name",
            '//*[@id="HEADING"]/text()'
        )
        loader.add_xpath(
            "address",
            '//*[@id="LOCATION"]/div[4]/div[1]/div[2]/span[2]/span/text()'
        )
        loader.add_xpath(
            "description",
            "//*[@id='ABOUT_TAB']/div[2]/div[1]/div[6]/@data-ssrev-handlers"
        )

        loader.add_xpath(
            "amenities",
            "//*[@id='ABOUT_TAB']/div[2]/div[2]/div[1]/@data-ssrev-handlers"
        )

        return loader.load_item()
