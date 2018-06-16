import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from likealyzer.items import LikealyzerItem
from selenium.webdriver.chrome.options import Options
import time
from scrapy.selector import Selector



class KeyholeSpider(CrawlSpider):

    name = 'likealyzer'


    def start_requests(self):
        allowed_domains = ['likealyzer.com']
        url = 'https://likealyzer.com/?lang=es'

        yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        
        likealyzer = LikealyzerItem()

        likealyzer['name'] = response.xpath('//a[@class="css-ovuman"]/text()').extract()

        yield likealyzer