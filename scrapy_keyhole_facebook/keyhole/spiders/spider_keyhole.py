import scrapy
import time

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.conf import settings
from selenium import webdriver
from keyhole.items import *
from selenium.webdriver.chrome.options import Options
import datetime
from scrapy.selector import Selector


class KeyholeSpiderFacebook(CrawlSpider):

    name = 'keyhole_facebook'

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

        yield scrapy.Request(url=url, callback=self.parseFacebook)

    def parseFacebook(self, response):

        keyhole = KeyholeFacebookItem()

        keyhole['source'] = self.name
        keyhole['platform'] = "Facebook"
        keyhole['name'] = self.searchName

        creationdate = getattr(self, 'time', None)
        if creationdate is not None:
            keyhole['date'] = datetime.datetime.strptime(creationdate,settings['DATE_FORMAT'])
        else:
            keyhole['date'] = datetime.datetime.strptime(str(datetime.datetime.now().isoformat()), settings['DATE_FORMAT'])


        keyhole['pageLikes'] = int(response.xpath('//div[@class="page-likes"]/p/text()').extract_first().replace(',','').replace('.','').replace('m','0000'))
        keyhole['averageLikesFacebook'] = int(response.xpath('//div[@class="avg-likes"]/p/text()').extract_first().replace(',',''))
        keyhole['averageComments'] = int(response.xpath('//div[@class="avg-comments"]/p/text()').extract_first().replace(',',''))
        keyhole['averageShares'] = int(response.xpath('//div[@class="avg-shares"]/p/text()').extract_first().replace(',',''))
        keyhole['averageEngagement'] = float(response.xpath('//div[@class="avg-engRate"]/p/text()').extract_first()[:-1])

        yield keyhole