import scrapy
from scrapy.loader import ItemLoader

from scrapy_selenium import SeleniumRequest

from tripadvisor.items import HotelItem
from tripadvisor.utils import dataloader



class HotelsSpider(scrapy.Spider):
    name = "hotels"

    def __init__(self, urls_filepath=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_urls = dataloader.read_xlsx(urls_filepath)
        self.start_urls = [self.start_urls[0]]

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)

    def parse(self, response, **kwargs):
        self.logger.info("First Spider working")

        loader = ItemLoader(item=HotelItem(), response=response)

        loader.add_xpath(
            "rating",
            '//*[@id="ABOUT_TAB"]/div[2]/div[1]/div[1]/span/text()'
        )
        loader.add_xpath(
            "review_count",
            '//*[@id="component_5"]/div/div/div[1]/div[2]/a/span[2]/text()'
        )
        loader.add_xpath(
            "unit_price",
            '//*[@id="bor_book_link_32457022"]/div/div[2]/div[1]/text()'
        )
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
