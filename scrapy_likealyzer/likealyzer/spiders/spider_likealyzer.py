import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.conf import settings 
from selenium import webdriver
from likealyzer.items import LikealyzerItem
from selenium.webdriver.chrome.options import Options

import datetime
from scrapy.selector import Selector



class KeyholeSpider(CrawlSpider):

    name = 'likealyzer'

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
        allowed_domains = ['likealyzer.com']
        url = 'https://likealyzer.com/?lang=es'

        yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        likealyzer = LikealyzerItem()

        likealyzer['source'] = self.name

        likealyzer['name'] = self.searchName
        likealyzer['platform'] = "Facebook"
        creationdate = getattr(self, 'time', None)
        if creationdate is not None:
            likealyzer['date'] = datetime.datetime.strptime(creationdate,settings['DATE_FORMAT'])
        else:
            likealyzer['date'] = datetime.datetime.strptime(str(datetime.datetime.now().isoformat()), settings['DATE_FORMAT'])

        likealyzer['summary'] = response.xpath('//div[@class="css-e80q00"]/span/text()').extract_first()
        likealyzer['comments'] = response.xpath('//ul[@class="css-6w6u3k"]/li/text()').extract()
        likealyzer['frontPage'] = int(response.xpath('//span[contains(text(),"Frontpage")]/following::span[1]/text()').extract_first().replace(" ","").replace("%","").replace("N/A","0"))
        likealyzer['about'] = int(response.xpath('//span[contains(text(),"About")]/following::span[1]/text()').extract_first().replace(" ","").replace("%","").replace("N/A","0"))
        likealyzer['activity'] = int(response.xpath('//span[contains(text(),"Activity")]/following::span[1]/text()').extract_first().replace(" ","").replace("%","").replace("N/A","0"))
        likealyzer['response'] = int(response.xpath('//span[contains(text(),"Response")]/following::span[1]/text()').extract_first().replace(" ","").replace("%","").replace("N/A","0"))
        likealyzer['engagement'] = int(response.xpath('//span[contains(text(),"Engagement")]/following::span[1]/span/text()').extract_first().replace(" ","").replace("%","").replace("N/A","0"))
        likealyzer['userPhotoAvailable'] = response.xpath('//div[@class="css-1roshqv"]/span/text()')[0].extract() 
        likealyzer['aboutAvailable'] = response.xpath('//div[@class="css-1roshqv"]/span/text()')[2].extract() 
        likealyzer['usernameAvailable'] = response.xpath('//div[@class="css-1roshqv"]/span/text()')[1].extract() 
        likealyzer['achievementsQuality'] = response.xpath('//div[@class="css-1roshqv"]/span/text()')[4].extract()
        likealyzer['contactInfoAvailable'] = response.xpath('//div[@class="css-1roshqv"]/span/text()')[5].extract()
        #likealyzer['elementsAvailable'] = response.xpath('//*[@class="css-80jabu"]/a/text()').extract()
        #likealyzer['elementsUnavailable'] = response.xpath('//div[@class="css-1cu89kn"]/text()').extract()

        likealyzer['phoneAvailable'] = response.xpath('//div[@class="css-63oe3q"]//*[self::a or self::div]/text()')[0].extract()
        likealyzer['websiteAvailable'] = response.xpath('//div[@class="css-63oe3q"]//*[self::a or self::div]/text()')[1].extract()
        likealyzer['emailAvailable'] = response.xpath('//div[@class="css-63oe3q"]//*[self::a or self::div]/text()')[2].extract()

        likealyzer['locationAvailable'] = response.xpath('//div[@class="css-1roshqv"]/span/text()')[6].extract()
        likealyzer['percentageOfPhotos'] = response.xpath('//div[@class="css-gy0z68"]/span[@class="css-13jkw0c"]/text()[1]')[0].extract()
        likealyzer['percentageOfNotes'] = response.xpath('//div[@class="css-gy0z68"]/span[@class="css-13jkw0c"]/text()[1]')[1].extract()
        likealyzer['percentageOfVideos'] = response.xpath('//div[@class="css-gy0z68"]/span[@class="css-13jkw0c"]/text()[1]')[2].extract()
        likealyzer['dailyMessages'] = response.xpath('//div[@class="css-1t98r4x"]//span/text()')[0].extract()
        likealyzer['messageLengthRatio'] = response.xpath('//div[@class="css-1t98r4x"]//span/text()')[1].extract()
        likealyzer['likedPages'] = response.xpath('//div[@class="css-1t98r4x"]//span/text()')[2].extract()
        likealyzer['originalFBVideos'] = response.xpath('//div[@class="css-1t98r4x"]//span/text()')[3].extract()
        likealyzer['usersCanPost'] = response.xpath('//div[@class="css-16l7y04"]//div/span/text()')[0].extract()
        likealyzer['answerToUsersRatio'] = response.xpath('//div[@class="css-16l7y04"]//div/span/text()')[1].extract()
        likealyzer['answerToUserResponseTime'] = response.xpath('//div[@class="css-16l7y04"]//div/span/text()')[2].extract()
        likealyzer['peopleTalking'] = int(response.xpath('//div[@class="css-1l0nltk"]//div/span/text()')[0].extract().replace(".",""))
        likealyzer['totalPageLikes'] = int(response.xpath('//div[@class="css-1l0nltk"]//div/span/text()')[1].extract().replace(".",""))
        likealyzer['participationRatio'] = response.xpath('//div[@class="css-1l0nltk"]//div/span/text()')[2].extract()

        yield likealyzer