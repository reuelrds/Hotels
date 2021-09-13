import os
import re

import scrapy
from scrapy.loader import ItemLoader

# from scrapy_selenium import SeleniumRequest

from tripadvisor.items import HotelItem
from tripadvisor.utils import dataloader

from urllib.parse import urlencode

from scraper_api import ScraperAPIClient


class HotelsSpider(scrapy.Spider):
    name = "hotels"

    def __init__(self, urls_filepath=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_urls = dataloader.read_xlsx(urls_filepath)
        self.start_urls = [self.start_urls[0]]
        self.client = ScraperAPIClient(os.environ["SCRAPPER_API_KEY"])

    def start_requests(self):
        for url in self.start_urls:
            self.logger.info(url)
            url = re.sub(r'www.', '', url)
            self.logger.info(url)
            # yield SeleniumRequest(url=HotelsSpider.get_scraperapi_url(url=url), callback=self.parse, wait_time=10)
            yield scrapy.http.Request(self.client.scrapyGet(url=url, render=True), callback=self.parse)

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
            '//*[@id="component_5"]/div/div/div[1]/div[2]/a/span[2]/text()'
        )
        # loader.add_xpath(
        #     "unit_price",
        #     '//*[@id="bor_book_link_32457022"]/div/div[2]/div[1]/text()'
        # )
        loader.add_xpath(
            "name",
            '//*[@id="HEADING"]/text()'
        )
        loader.add_xpath(
            "address",
            '//*[@id="component_5"]/div/div/div[2]/div/div[2]/div/div/div/span[2]/span/text()'
        )
        loader.add_xpath(
            "description",
            '//*[@id="ABOUT_TAB"]/div[2]/div[2]/div[1]/div/div[1]/text()'
        )

        # loader.add_xpath(
        #     "amenities",
        #     "//*[@id='ABOUT_TAB']/div[2]/div[2]/div[1]/@data-ssrev-handlers"
        # )

        return loader.load_item()

    @staticmethod
    def get_scraperapi_url(url):
        payload = {'api_key': os.environ["SCRAPPER_API_KEY"], 'url': url}
        proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
        return proxy_url
