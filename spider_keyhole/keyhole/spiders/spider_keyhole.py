import scrapy
import time

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from keyhole.items import KeyholeItem
from selenium.webdriver.chrome.options import Options
import datetime
from scrapy.selector import Selector



class KeyholeSpider(CrawlSpider):

    name = 'keyhole'


    def start_requests(self):
        allowed_domains = ['keyhole.co']
        url = 'http://keyhole.co/'

        yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        
        keyhole = KeyholeItem()
        
        keyhole['name'] = response.xpath('/html/body/div[1]/section/div[2]/main/figure[1]/div/div[1]/div/div[2]/div/a/p/text()').extract_first()
        keyhole['date'] = datetime.datetime.utcnow()
        keyhole['tweets'] = int(response.xpath('//div[@class="posts"]/p/text()').extract_first())
        keyhole['followers'] = int(response.xpath('//div[@class="followers"]/p/text()').extract_first())
        keyhole['following'] = int(response.xpath('//div[@class="following"]/p/text()').extract_first())
        keyhole['avgRetweets'] = int(response.xpath('//div[@class="avg-likes"]/p/text()').extract_first())
        keyhole['avgLikes'] = int(response.xpath('//div[@class="avg-retweets"]/p/text()').extract_first())
        keyhole['engRate'] = float(response.xpath('//div[@class="avg-engRate"]/p/text()').extract_first())
        keyhole['website'] = response.xpath('//a[@class="website"]/text()').extract_first()
        

        #keyhole['bio'] = updatedPage.xpath('//p[@class="bio"]/span/text()').extract_first()

        yield keyhole