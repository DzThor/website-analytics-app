import scrapy
import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from socialmention.items import SocialmentionItem
from scrapy.selector import Selector


class SocialmentionSpider(CrawlSpider):

    name = 'socialmention'

    def start_requests(self):

        url = 'http://socialmention.com/search?q=iphone+apps'

        yield scrapy.Request(url=url, callback=self.parse, dont_filter = True)


    def eraseDifferentLevelTags(self,response,expression):
        
        #cleanTags = list()
        dictTags = dict()

        tags = expression + "/a/text()"
        tagsCont = expression + "/text()"
        #for element in response.xpath(expression):
        #    if(element.xpath('./a')):
        #        cleanTags.append(element.xpath('a/text()').extract_first())
        #    else:
        #        cleanTags.append(element.xpath('text()').extract_first())

        for tagElement, tagValue in zip(response.xpath(tags).extract(), response.xpath(tagsCont).extract()):
            dictTags[tagElement] = tagValue
            
        return dictTags
        #return cleanTags

    def parse(self, response):
            
        socialIt = SocialmentionItem()

        socialIt['name'] = response.xpath('//div[@id="column_middle"]/h2/b/text()').extract_first()
        socialIt['date'] = datetime.datetime.utcnow()
        socialIt['strengh'] = response.xpath('//div[@class="score"]/text()')[0].extract()
        socialIt['sentimentRatio'] = response.xpath('//div[@class="score"]/text()')[1].extract()
        socialIt['passion'] = response.xpath('//div[@class="score"]/text()')[2].extract()
        socialIt['reach'] = response.xpath('//div[@class="score"]/text()')[3].extract()
        socialIt['timePerMention'] = response.xpath('//div[@class="box grey text"]/text()')[0].extract()
        socialIt['lastMention'] = response.xpath('//div[@class="box grey text"]/text()')[1].extract()
        socialIt['uniqueAuthors'] = response.xpath('//div[@class="box grey text"]/text()')[2].extract()
        socialIt['retweets'] = response.xpath('//div[@class="box grey text"]/text()')[3].extract()

        #Llamamos una función para sacar el contenido de los nodos, ya que contienen distintos niveles

        socialIt['sentimentValues'] = self.eraseDifferentLevelTags(response,'//h4[contains(text(),"Sentiment")]/following-sibling::table//td[contains(@width,25) or contains(@width,90)]')
        socialIt['keywordsValues'] = self.eraseDifferentLevelTags(response,'//h4[contains(text(),"Top Keywords")]/following-sibling::table//*[contains(@width,25) or contains(@width,90)]')
        socialIt['usersValues'] = self.eraseDifferentLevelTags(response,'//h4[contains(text(),"Top Users")]/following-sibling::table//*[contains(@width,25) or contains(@width,90)]')
        socialIt['hashtagsValues'] = self.eraseDifferentLevelTags(response,'//h4[contains(text(),"Top Hashtags")]/following-sibling::table//*[contains(@width,25) or contains(@width,90)]')

        
        yield socialIt