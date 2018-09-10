import scrapy
import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.conf import settings
from socialmention.items import SocialmentionItem
from scrapy.selector import Selector


class SocialmentionSpider(CrawlSpider):

    name = 'socialmention'

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

        url = 'http://socialmention.com/search?q=' + self.searchName

        yield scrapy.Request(url=url, callback=self.parse, dont_filter = True)


    def createTagsDict(self,response,expression):

        dictTags = dict()

        tags = expression + "/a/text()"
        tagsCont = expression + "/text()"

        for tagElement, tagValue in zip(response.xpath(tags).extract(), response.xpath(tagsCont).extract()):
            dictTags[tagElement] = tagValue

        return dictTags

    def parse(self, response):

        socialIt = SocialmentionItem()

        socialIt['source'] = self.name

        socialIt['name'] = self.searchName
        socialIt['platform'] = "Internet"

        creationdate = getattr(self, 'time', None)
        if creationdate is not None:
            socialIt['date'] = datetime.datetime.strptime(creationdate,settings['DATE_FORMAT'])
        else:
            socialIt['date'] = datetime.datetime.strptime(str(datetime.datetime.now().isoformat()), settings['DATE_FORMAT'])

        socialIt['strength'] = int(response.xpath('//div[@class="score"]/text()')[0].extract())
        socialIt['sentiment'] = int(response.xpath('//div[@class="score"]/text()')[1].extract().split(":")[0])
        socialIt['passion'] = int(response.xpath('//div[@class="score"]/text()')[2].extract())
        socialIt['reach'] = int(response.xpath('//div[@class="score"]/text()')[3].extract())
        socialIt['timePerMention'] = response.xpath('//div[@class="box grey text"]/text()')[0].extract()
        socialIt['lastMention'] = response.xpath('//div[@class="box grey text"]/text()')[1].extract()
        socialIt['uniqueAuthors'] = response.xpath('//div[@class="box grey text"]/text()')[2].extract()
        socialIt['retweets'] = response.xpath('//div[@class="box grey text"]/text()')[3].extract()

        #Llamamos una función para sacar el contenido de los nodos, ya que contienen distintos niveles

        socialIt['sentimentValues'] = self.createTagsDict(response,'//h4[contains(text(),"Sentiment")]/following-sibling::table//td[contains(@width,25) or contains(@width,90)]')
        socialIt['keywordsValues'] = self.createTagsDict(response,'//h4[contains(text(),"Top Keywords")]/following-sibling::table//*[contains(@width,25) or contains(@width,90)]')
        socialIt['usersValues'] = self.createTagsDict(response,'//h4[contains(text(),"Top Users")]/following-sibling::table//*[contains(@width,25) or contains(@width,90)]')
        socialIt['hashtagsValues'] = self.createTagsDict(response,'//h4[contains(text(),"Top Hashtags")]/following-sibling::table//*[contains(@width,25) or contains(@width,90)]')

        yield socialIt