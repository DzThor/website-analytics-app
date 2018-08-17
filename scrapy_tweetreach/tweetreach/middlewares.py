# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging
from selenium.webdriver.remote.remote_connection import LOGGER

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as exceptions


class TweetreachSpiderMiddleware(object):
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


class TweetreachDownloaderMiddleware(object):
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

        username = settings["TWITTER_ACCOUNT"]
        password = settings["TWITTER_PASS"]

        self.driver.get('https://tweetreach.com/')

        self.driver.find_element_by_xpath('//input[@class="search-form__input"]').click()
        searchElement = self.driver.find_element_by_xpath('//input[@class="search-form__input"]')
        searchElement.send_keys(spider.searchName)

        time.sleep(2)

        self.driver.find_element_by_xpath('//input[@class="search-form__button"]').click()

        time.sleep(5)


        #Introducir cosas de twitter

        #usuario //*[@id="username_or_email"]
        searchElement = self.driver.find_element_by_xpath('//*[@id="username_or_email"]')
        searchElement.send_keys(username)
        #pass //*[@id="password"]
        searchElement = self.driver.find_element_by_xpath('//*[@id="password"]')
        searchElement.send_keys(password)

        #boton //*[@id="allow"]
        self.driver.find_element_by_xpath('//*[@id="allow"]').click()

        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH,'//div[@class="query" and text() != ""]')))
        except exceptions.TimeoutException:
            raise Exception('Unable to find text in this element after waiting 20 seconds')

        body = self.driver.page_source
        currentUrl = self.driver.current_url

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