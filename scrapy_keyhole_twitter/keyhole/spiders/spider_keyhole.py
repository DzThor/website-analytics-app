import scrapy
import time

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.conf import settings
from selenium import webdriver
from keyhole.items import KeyholeTwitterItem
from selenium.webdriver.chrome.options import Options
import datetime
from scrapy.selector import Selector



class KeyholeSpiderTwitter(CrawlSpider):

    name = 'keyhole_twitter'

    def __init__(self, time='', searchname='', **kwargs):

        try:
            self.searchName = searchname
            if not self.searchName:
                raise ValueError('El campo de búsqueda en config.json está vacío')
        except ValueError as e:
            print(e)
            raise e

        try:
            self.time = time
            if not self.time:
                raise ValueError('El campo de fecha en la llamada está vacío')
        except ValueError as e:
            print(e)
            raise e

        super().__init__(**kwargs)  # python3

    def start_requests(self):
        url = 'http://keyhole.co/'

        yield scrapy.Request(url=url, callback=self.parseTwitter, meta={'platformChosen': 'Twitter'})


    def parseTwitter(self, response):

        keyhole = KeyholeTwitterItem()

        keyhole['source'] = self.name
        keyhole['platform'] = "Twitter"
        keyhole['name'] = self.searchName


        creationdate = getattr(self, 'time', None)
        if creationdate is not None:
            keyhole['date'] = datetime.datetime.strptime(creationdate,settings['DATE_FORMAT'])
        else:
            keyhole['date'] = datetime.datetime.strptime(str(datetime.datetime.now().isoformat()), settings['DATE_FORMAT'])


        keyhole['tweets'] = int(response.xpath('//div[@class="posts"]/p/text()').extract_first().replace(',',''))
        keyhole['followers'] = int(response.xpath('//div[@class="followers"]/p/text()').extract_first().replace(',','').replace('.','').replace('m','0000'))
        keyhole['following'] = int(response.xpath('//div[@class="following"]/p/text()').extract_first().replace(',',''))
        keyhole['avgRetweets'] = int(response.xpath('//div[@class="avg-likes"]/p/text()').extract_first().replace(',',''))
        keyhole['avgLikes'] = int(response.xpath('//div[@class="avg-retweets"]/p/text()').extract_first().replace(',',''))
        keyhole['engRate'] = float(response.xpath('//div[@class="avg-engRate"]/p/text()').extract_first()[:-1])
        keyhole['website'] = response.xpath('//a[@class="website"]/text()').extract_first()


        #keyhole['bio'] = updatedPage.xpath('//p[@class="bio"]/span/text()').extract_first()

        yield keyhole
