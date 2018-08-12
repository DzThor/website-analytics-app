# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging
from selenium.webdriver.remote.remote_connection import LOGGER


class KeyholeSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class KeyholeDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self):

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--lang=en")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--mute-all")

        LOGGER.setLevel(logging.WARNING)

        self.driver = webdriver.Chrome(chrome_options=chrome_options)
    
    def __del__(self):
        self.driver.close()

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        

        self.driver.get('http://keyhole.co/')


        self.driver.find_element_by_xpath('/html/body/div[1]/main/section[1]/div/div/div/div/a[2]').click()
        time.sleep(4)

        buttonTwitter = self.driver.find_element_by_xpath('//*[@id="twt_check" and contains(@name,"platform_acc")]')
        buttonTwitter.click()

        self.driver.find_element_by_xpath('//form[@class="account-tracking-form form-active"]/div/input[@id="search"]').click()
        searchElement = self.driver.find_element_by_xpath('//form[@class="account-tracking-form form-active"]/div/input[@id="search"]')
        searchElement.send_keys("Stargate")
        time.sleep(1)

        self.driver.find_element_by_xpath('//input[@id="letsgo"]').click()
        time.sleep(5)
        
        body = self.driver.page_source
        currentUrl = self.driver.current_url
        #self.driver.close()

        return HtmlResponse(currentUrl, body=body, encoding='utf-8', request=request)




    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
