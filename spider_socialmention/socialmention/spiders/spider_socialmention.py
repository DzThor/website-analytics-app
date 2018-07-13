import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from socialmention.items import SocialmentionItem
from scrapy.selector import Selector


class SocialmentionSpider(CrawlSpider):

    name = 'socialmention'

    def start_requests(self):
        allowed_domains = ['socialmention.com']
        url = 'http://socialmention.com/search?q=iphone+apps'

        yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
            
        socialIt = SocialmentionItem()

        socialIt['name'] = response.xpath('//div[@id="column_middle"]/h2/b/text()').extract_first()
        socialIt['strengh'] = response.xpath('//div[@class="score"]/text()')[0].extract()
        socialIt['sentimentRatio'] = response.xpath('//div[@class="score"]/text()')[1].extract()
        socialIt['passion'] = response.xpath('//div[@class="score"]/text()')[2].extract()
        socialIt['reach'] = response.xpath('//div[@class="score"]/text()')[3].extract()
        socialIt['timePerMention'] = response.xpath('normalize-space(//div[@class="box grey text"]/text())')[0].extract()
        socialIt['lastMention'] = response.xpath('normalize-space(//div[@class="box grey text"]/text())')[1].extract()
        socialIt['uniqueAuthors'] = response.xpath('normalize-space(//div[@class="box grey text"]/text())')[2].extract()
        socialIt['retweets'] = response.xpath('normalize-space(//div[@class="box grey text"]/text())')[3].extract()

        yield socialIt