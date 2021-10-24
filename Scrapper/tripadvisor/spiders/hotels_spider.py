import os
import re
import time

import scrapy
from scrapy.loader import ItemLoader

from scrapy_selenium import SeleniumRequest

from tripadvisor import settings

from tripadvisor.items import HotelItem
from tripadvisor.utils import dataloader

from urllib.parse import urlencode

# from scraper_api import ScraperAPIClient


class HotelsSpider(scrapy.Spider):
    name = "hotels"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hotels = dataloader.read_xlsx(settings.URLs_FILEPATH)

    def start_requests(self):
        for hotel_id, url in self.hotels:
            self.logger.info(url)
            # url = HotelsSpider.get_scraperapi_url(url=url)
            self.logger.info(url)

            yield SeleniumRequest(wait_time=10, url=url, callback=self.parse, cb_kwargs={"Hotel ID": hotel_id})

    def parse(self, response, **kwargs):
        self.logger.info("First Spider working")

        loader = ItemLoader(item=HotelItem(), response=response)

        with open('page.html', 'wb') as html_file:
            html_file.write(response.body)

        loader.add_xpath(
            "rating",
            '//*[@id="ABOUT_TAB"]/div[2]/div[1]/div[1]/span/text()'
        )
        loader.add_xpath(
            "review_count",
            '//*[@id="ABOUT_TAB"]/div[2]/div[1]/div[1]/a/span[2]/text()'
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
            '//*[@id="component_5"]/div/div/div[2]/div/div[2]/div/div/div/span[2]/span/text()'
        )
        loader.add_xpath(
            "address",
            '//*[@id="component_4"]/div/div[1]/div[2]/div/div[2]/div/div/div/span[2]/span/text()'
        )

        loader.add_xpath(
            "description",
            "//*[@id='ABOUT_TAB']/div[2]/div[1]/div[2]/@data-ssrev-handlers"
        )
        loader.add_css(
            "description",
            '.duhwe._T.bOlcm.bWqJN.Ci.dMbup > .pIRBV._T'
        )

        loader.add_value("hotel_id", kwargs.get("Hotel ID"))

        # loader.add_xpath(
        #     "amenities",
        #     "//*[@id='ABOUT_TAB']/div[2]/div[2]/div[1]/@data-ssrev-handlers"
        # )

        return loader.load_item()

    @staticmethod
    def get_scraperapi_url(url):
        payload = {
            "api_key": os.environ["SCRAPPER_API_KEY"], "url": url, "country_code": "us"}
        proxy_url = "http://api.scraperapi.com/?" + \
            urlencode(payload)

        print(f"PROXY URL: {proxy_url}")
        return proxy_url
