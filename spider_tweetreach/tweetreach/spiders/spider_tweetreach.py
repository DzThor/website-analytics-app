import scrapy
import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tweetreach.items import TweetreachItem

class TweetreachSpider(CrawlSpider):
    name = 'tweetreach'
    
    def start_requests(self):

        url = 'https://tweetreach.com'
        
        yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        
        tw_item = TweetreachItem()

        tw_item['username'] = response.xpath('//div[@class="query"]/text()').extract_first()
        tw_item['date'] = datetime.datetime.utcnow()
        tw_item['estimated_reach'] = response.xpath('//div[@class="reach_score data_number"]/text()').extract_first()
        tw_item['impressions'] =response.xpath('//div[@class="exposure_impressions data_number"]/text()').extract_first()
        tw_item['top_contributors'] = response.xpath('//div[@class="number_box mini show_tooltip" or @class="info"]/span[@class = "number"]/text()').extract_first()
        yield tw_item
        