import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from keyhole.items import KeyholeItem
from selenium.webdriver.chrome.options import Options
import time
from scrapy.selector import Selector



class KeyholeSpider(CrawlSpider):

    name = 'keyhole'


    def start_requests(self):
        allowed_domains = ['keyhole.co']
        url = 'http://keyhole.co/'

        yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        
        keyhole = KeyholeItem()
        
        keyhole['name'] = response.xpath('/html/body/div[1]/section/div[2]/main/figure[1]/div/div[1]/div/div[2]/div/a/p/text()').extract()[-1]
        keyhole['posts'] = response.xpath('//div[@class="posts"]/p/text()').extract()[-1]
        keyhole['followers'] = response.xpath('//div[@class="followers"]/p/text()').extract()[-1]
        keyhole['following'] = response.xpath('//div[@class="following"]/p/text()').extract()[-1]
        keyhole['avgRetweets'] = response.xpath('//div[@class="avg-likes"]/p/text()').extract()[-1]
        keyhole['avgLikes'] = response.xpath('//div[@class="avg-retweets"]/p/text()').extract()[-1]
        keyhole['engRate'] = response.xpath('//div[@class="avg-engRate"]/p/text()').extract()[-1]
        keyhole['website'] = response.xpath('//a[@class="website"]/text()').extract()[-1]

        #keyhole['bio'] = updatedPage.xpath('//p[@class="bio"]/span/text()').extract()

        yield keyhole