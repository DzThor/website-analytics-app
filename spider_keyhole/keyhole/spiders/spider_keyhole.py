import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from keyhole.items import KeyholeItem
from selenium.webdriver.chrome.options import Options
import time
from scrapy.selector import Selector



class KeyholeSpider(CrawlSpider):

    name = 'keyhole'

    def start_requests(self):
        allowed_domains = ['keyhole.co']
        url = 'http://keyhole.co/'

        yield scrapy.Request(url=url, callback=self.parse)



    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")

        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def parse(self, response):
        
        keyhole = KeyholeItem()
        self.driver.get(response.url)

        self.driver.find_element_by_xpath('/html/body/div[1]/main/section[1]/div/div/div/div/a[2]').click()
        
        time.sleep(2)

        self.driver.find_element_by_xpath('//form[@class="account-tracking-form form-active"]/div/input[@id="search"]').click()
        searchElement = self.driver.find_element_by_xpath('//form[@class="account-tracking-form form-active"]/div/input[@id="search"]')
        searchElement.send_keys("Stargate")
        
        time.sleep(2)

        self.driver.find_element_by_xpath('//input[@id="letsgo"]').click()
        
        time.sleep(5)

        updatedPage = Selector(text=self.driver.page_source)
        
        keyhole['name'] = updatedPage.xpath('/html/body/div[1]/section/div[2]/main/figure[1]/div/div[1]/div/div[2]/div/a/p/text()').extract()[-1]
        keyhole['posts'] = updatedPage.xpath('//div[@class="posts"]/p/text()').extract()[-1]
        keyhole['followers'] = updatedPage.xpath('//div[@class="followers"]/p/text()').extract()[-1]
        keyhole['following'] = updatedPage.xpath('//div[@class="following"]/p/text()').extract()[-1]
        keyhole['avgRetweets'] = updatedPage.xpath('//div[@class="avg-likes"]/p/text()').extract()[-1]
        keyhole['avgLikes'] = updatedPage.xpath('//div[@class="avg-retweets"]/p/text()').extract()[-1]
        keyhole['engRate'] = updatedPage.xpath('//div[@class="avg-engRate"]/p/text()').extract()[-1]
        keyhole['website'] = updatedPage.xpath('//a[@class="website"]/text()').extract()[-1]

        #keyhole['bio'] = updatedPage.xpath('//p[@class="bio"]/span/text()').extract()

        self.driver.close()

        yield keyhole