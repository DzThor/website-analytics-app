import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from foller.items import FollerItem
import requests

class FollerSpider(CrawlSpider):
    name = 'foller'
    
    def start_requests(self):
        allowed_domains = ['www.foller.me']
        url = 'https://foller.me'

        yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        
        fl_item = FollerItem()
        fl_item['username'] = response.xpath('/html/body/div[3]/div/div/div[2]/div/h1/small/text()').extract()
        fl_item['tweets'] = response.xpath('//*[@id="overview"]/div[2]/div[4]/table/tbody/tr[1]/td[2]/text()').extract()
        fl_item['followers'] = response.xpath('//*[@id="overview"]/div[2]/div[4]/table/tbody/tr[2]/td[2]/text()').extract()
        fl_item['following'] = response.xpath('//*[@id="overview"]/div[2]/div[4]/table/tbody/tr[3]/td[2]/text()').extract()
        fl_item['followers_ratio'] = response.xpath('//*[@id="overview"]/div[2]/div[4]/table/tbody/tr[4]/td[2]/text()').extract()
        fl_item['topics'] = response.xpath("//a[contains(@class, 'tag-cloud-link')]/text()").extract()
        fl_item['hashtags'] = response.xpath('//div[@class="span12"]/p/a[contains(text(),"#")]/text()').extract()
        #fl_item['xtweets'] = response.xpath('//section[@id="tweets"]/div/div[@class="span4"]/h2/text()').extract_first()
        fl_item['replies_for_xtweets'] = response.xpath('normalize-space(//td[contains(text(),"Replies")]/following::td[1])').extract_first()
        fl_item['mentions_for_xtweets'] = response.xpath('normalize-space(//td[contains(text(),"Tweets with @mentions")]/following-sibling::td[1])').extract()
        fl_item['hashtags_for_xtweets'] = response.xpath('normalize-space(//td[contains(text(),"Tweets with #hashtags")]/following-sibling::td[1])').extract()
        fl_item['retweets_for_xtweets'] = response.xpath('normalize-space(//td[contains(text(),"Retweets")]/following-sibling::td[1])').extract()
        fl_item['links_for_xtweets'] = response.xpath('normalize-space(//td[contains(text(),"Tweets with links")]/following-sibling::td[1])').extract()
        fl_item['media_for_xtweets'] = response.xpath('normalize-space(//td[contains(text(),"Tweets with media")]/following-sibling::td[1])').extract()
        fl_item['linked_domains_for_xtweets'] = response.xpath('normalize-space(//td[contains(text(),"Most linked domains")]/following-sibling::td[1])').extract()
        fl_item['twitter_clients_for_xtweets'] = response.xpath('normalize-space(//td[contains(text(),"Twitter clients usage")]/following-sibling::td[1])').extract()
        
        yield fl_item
        


