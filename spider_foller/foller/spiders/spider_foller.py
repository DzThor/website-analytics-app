import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from foller.items import FollerItem

class FollerSpider(CrawlSpider):
    name = 'foller'
    
    def start_requests(self):
        allowed_domains = ['www.foller.me']
        urls = ['https://foller.me/pokemon']
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        
        fl_item = FollerItem()
        fl_item['username'] = response.xpath('/html/body/div[3]/div/div/div[2]/div/h1/small').extract()
        fl_item['tweets'] = response.xpath('//*[@id="overview"]/div[2]/div[4]/table/tbody/tr[1]/td[2]').extract()
        fl_item['followers'] = response.xpath('//*[@id="overview"]/div[2]/div[4]/table/tbody/tr[2]/td[2]').extract()
        fl_item['following'] = response.xpath('//*[@id="overview"]/div[2]/div[4]/table/tbody/tr[3]/td[2]').extract()
        fl_item['followers_ratio'] = response.xpath('//*[@id="overview"]/div[2]/div[4]/table/tbody/tr[4]/td[2]').extract()
        fl_item['topics'] = response.xpath("//p[@id = 'topics-cloud']").extract()
        fl_item['hashtags'] = response.xpath('//*[@id="topics"]/div[3]/div[2]/p').extract()
        fl_item['replies_100'] = response.xpath('(//*[@id="tweets"]/div[2]/div[2]/table/tbody/tr[1]/td[2]').extract()
        fl_item['mentions_100'] = response.xpath('(//*[@id="tweets"]/div[2]/div[2]/table/tbody/tr[2]/td[2]').extract()
        fl_item['hashtags_100'] = response.xpath('(//*[@id="tweets"]/div[2]/div[2]/table/tbody/tr[3]/td[2]').extract()
        fl_item['retweets_100'] = response.xpath('(//*[@id="tweets"]/div[2]/div[2]/table/tbody/tr[4]/td[2]').extract()
        fl_item['links_100'] = response.xpath('(//*[@id="tweets"]/div[2]/div[2]/table/tbody/tr[5]/td[2]').extract()
        fl_item['media_100'] = response.xpath('(//*[@id="tweets"]/div[2]/div[2]/table/tbody/tr[6]/td[2]').extract()
        fl_item['linked_domains_100'] = response.xpath('(//*[@id="tweets"]/div[2]/div[2]/table/tbody/tr[7]/td[2]').extract()
        fl_item['twitter_clients_100'] = response.xpath('(//*[@id="tweets"]/div[2]/div[2]/table/tbody/tr[8]/td[2]').extract()
        
        yield fl_item
        


