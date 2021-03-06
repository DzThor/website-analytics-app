import scrapy
import requests

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.conf import settings
from foller.items import FollerItem
import datetime

class FollerSpider(CrawlSpider):
    name = 'foller'

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

        url = 'https://foller.me'

        yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        follerData = FollerItem()
        follerData['source'] = self.name
        follerData['platform'] = "Twitter"
        follerData['name'] = self.searchName

        creationdate = self.time
        if creationdate is not None:
            follerData['date'] = datetime.datetime.strptime(creationdate,settings['DATE_FORMAT'])
        else:
            follerData['date'] = datetime.datetime.strptime(str(datetime.datetime.now().isoformat()), settings['DATE_FORMAT'])

        follerData['tweets'] = int(response.xpath('//*[@id="overview"]/div[2]/div[4]/table/tbody/tr[1]/td[2]/text()').extract_first().replace(',', ''))
        follerData['followers'] = int(response.xpath('//*[@id="overview"]/div[2]/div[4]/table/tbody/tr[2]/td[2]/text()').extract_first().replace(',', ''))
        follerData['following'] = int(response.xpath('//*[@id="overview"]/div[2]/div[4]/table/tbody/tr[3]/td[2]/text()').extract_first().replace(',', ''))
        follerData['followers_ratio'] = float(response.xpath('//*[@id="overview"]/div[2]/div[4]/table/tbody/tr[4]/td[2]/text()').extract_first())
        follerData['topics'] = response.xpath("//a[contains(@class, 'tag-cloud-link')]/text()").extract()
        follerData['hashtags'] = response.xpath('//div[@class="span12"]/p/a[contains(text(),"#")]/text()').extract()

        xtweets = response.xpath('//*[@id="tweets"]/div[2]/div[1]/h2/text()').extract_first()
        follerData['xtweets'] = int(xtweets.split()[0])

        follerData['replies_for_xtweets'] = int(response.xpath('normalize-space(//td[contains(text(),"Replies")]/following::td[1]/text())').extract_first())
        follerData['mentions_for_xtweets'] = int(response.xpath('normalize-space(//td[contains(text(),"Tweets with @mentions")]/following-sibling::td[1]/text())').extract_first())
        follerData['hashtags_for_xtweets'] = int(response.xpath('normalize-space(//td[contains(text(),"Tweets with #hashtags")]/following-sibling::td[1]/text())').extract_first())

        retweets_xtweets = response.xpath('normalize-space(//td[contains(text(),"Retweets")]/following-sibling::td[1]/text())').extract_first()
        follerData['retweets_for_xtweets'] = int(retweets_xtweets[:7])

        follerData['links_for_xtweets'] = int(response.xpath('normalize-space(//td[contains(text(),"Tweets with links")]/following-sibling::td[1]/text())').extract_first())
        follerData['media_for_xtweets'] = int(response.xpath('normalize-space(//td[contains(text(),"Tweets with media")]/following-sibling::td[1]/text())').extract_first())
        follerData['linked_domains_for_xtweets'] = response.xpath('normalize-space(//td[contains(text(),"Most linked domains")]/following-sibling::td[1])').extract()[0].replace(" ", "").split(",")
        follerData['twitter_clients_for_xtweets'] = response.xpath('normalize-space(//td[contains(text(),"Twitter clients usage")]/following-sibling::td[1])').extract()[0].split(",")

        scheduleValues = []
        timelabels = response.xpath('//div[@class="hours"]/div/span/text()').extract()
        timeRows = response.xpath('//div[@class="hours"]/div/a/@data-original-title').extract()

        for row in range(0,len(timelabels)):
            scheduleValues.append([timelabels[row],timeRows[row].replace(" tweets", "").replace(" tweet","")])

        follerData['tweetingSchedule'] = scheduleValues
        yield follerData



